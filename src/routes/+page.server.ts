import { fail } from '@sveltejs/kit';
import { buildFeatureIndex, movieToVector, profileToVector, scoreAllMovies } from './recommend';
import type { SupabaseClient } from '@supabase/supabase-js';
import type { PageServerLoad } from './$types';

const TMDB_API_KEY =
	'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkMWM4ZWZhZjE5ODhjODNjZjBjNDRjOTk0ODczY2QzNiIsIm5iZiI6MTc0NTI1NjU4OS43MzMsInN1YiI6IjY4MDY4MDhkYWMwMmQ0NDA3YmFhZDI0YyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.JojH5OScAMuADI0hcoCt7CvtRwBeQRwj65klaDW4uPk';

const fetchMoviesFromSupabase = async (supabase: SupabaseClient) => {
	const { data, error } = await supabase
		.from('movies')
		.select('*')
		.order('release_date', { ascending: false });

	if (error) {
		throw new Error(`Failed to fetch movies from Supabase: ${error.message}`);
	}

	return data;
};

const fetchGenresFromTMDB = async () => {
	const url = 'https://api.themoviedb.org/3/genre/movie/list?language=en-US';
	const res = await fetch(url, {
		headers: {
			accept: 'application/json',
			Authorization: TMDB_API_KEY
		}
	});

	if (!res.ok) {
		throw new Error(`Failed to fetch genres from TMDB: ${res.status}`);
	}

	const data = await res.json();
	return new Map(data.genres.map((genre: { id: number; name: string }) => [genre.id, genre.name]));
};

const fetchUserPreferences = async (supabase: SupabaseClient, user_id: string) => {
	const { data, error } = await supabase
		.from('user_preferences_cache')
		.select('*')
		.eq('profile_id', user_id)
		.single();

	if (error || !data) {
		throw new Error('User preferences not found');
	}

	return {
		genres: data.genres || {},
		keywords: data.keywords || {},
		actors: data.actors || {},
		directors: data.directors || {}
	};
};

export const load: PageServerLoad = async ({ url, locals: { safeGetSession, supabase } }) => {
	const { session } = await safeGetSession();

	if (!session) {
		return {
			url: url.origin,
			session: null,
			movies: []
		};
	}

	try {
		const user_id = session.user.id;

		const [rawMovies, genreMap, userPrefs] = await Promise.all([
			fetchMoviesFromSupabase(supabase),
			fetchGenresFromTMDB(),
			fetchUserPreferences(supabase, user_id)
		]);

		const stats: { df: Record<string, number>; totalDocs: number } = {
			df: {},
			totalDocs: rawMovies.length
		};

		for (const m of rawMovies) {
			const seen = new Set<string>();
			for (const t of [...(m.genres ?? []), ...(m.keywords ?? []), ...(m.cast_names ?? []), ...(m.director_names ?? [])]) {
				if (!seen.has(t)) {
					stats.df[t] = (stats.df[t] || 0) + 1;
					seen.add(t);
				}
			}
		}

		const { indexMap, size: totalDim } = buildFeatureIndex(rawMovies);
		const movieVectors: Record<string, Float32Array> = {};
		for (const m of rawMovies) {
			movieVectors[m.id] = movieToVector(m, stats, indexMap, totalDim);
		}

		const userVec = profileToVector(userPrefs, stats, indexMap, totalDim);

		const movieMeta: Record<string, { vote_average: number; vote_count: number }> = {};
		for (const m of rawMovies) {
			movieMeta[m.id] = {
				vote_average: m.vote_average ?? 0,
				vote_count: m.vote_count ?? 0
			};
		}

		const scoredMovies = scoreAllMovies(userVec, movieVectors, movieMeta)
			.sort((a, b) => b.score - a.score)
			.slice(0, 200)
			.map(({ movieId, score }) => {
				const m = rawMovies.find((movie) => movie.id === movieId);
				if (!m) {
					console.error(`Movie with ID ${movieId} not found in rawMovies`);
					return null;
				}

				return {
					title: m.title,
					year: new Date(m.release_date).getFullYear().toString(),
					poster: m.poster_url,
					description: m.description,
					genres: (m.genres || []).map((gid: string) => genreMap.get(parseInt(gid)) || gid),
					actors: m.cast_names || [],
					director: m.director_names || [],
					movie_id: m.id,
					score
				};
			})
			.filter((movie) => movie !== null);

		return {
			url: url.origin,
			session,
			movies: scoredMovies
		};
	} catch (error: any) {
		console.error('Error in load function:', error);
		return fail(500, { message: 'Failed to load movies', error: error.message });
	}
};
