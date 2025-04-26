// recommend.ts
export interface MovieRaw {
	id: string;
	genres: string[];
	keywords: string[];
	cast_names: string[];
	director_names: string[];
}

export interface UserPrefsRaw {
	genres: Record<string, number>;
	keywords: Record<string, number>;
	actors: Record<string, number>;
	directors: Record<string, number>;
}

export interface TfIdfStats {
	df: Record<string, number>;
	totalDocs: number;
}

export type Vector = Float32Array;

function tfidf(term: string, stats: TfIdfStats): number {
	const df = stats.df[term] ?? 0;
	if (df === 0) return 0;
	return Math.log(1 + stats.totalDocs / df);
}

function normalize(v: Vector): void {
	let sumSq = 0;
	for (let i = 0; i < v.length; i++) sumSq += v[i] * v[i];
	const invLen = sumSq > 0 ? 1 / Math.sqrt(sumSq) : 0;
	for (let i = 0; i < v.length; i++) v[i] *= invLen;
}

function cosine(u: Vector, v: Vector): number {
	let dot = 0;
	for (let i = 0; i < u.length; i++) dot += u[i] * v[i];
	return dot;
}

export function buildFeatureIndex(movies: MovieRaw[]): {
	indexMap: Record<string, number>;
	size: number;
} {
	const idx: Record<string, number> = {};
	let counter = 0;
	for (const m of movies) {
		for (const t of [...m.genres, ...m.keywords, ...m.cast_names, ...m.director_names]) {
			if (idx[t] === undefined) idx[t] = counter++;
		}
	}
	return { indexMap: idx, size: counter };
}

export function movieToVector(
	movie: MovieRaw,
	stats: TfIdfStats,
	indexMap: Record<string, number>,
	totalDim: number
): Vector {
	const v = new Float32Array(totalDim);
	const addTerms = (terms: string[], weight: number) => {
		for (const t of terms) {
			const idx = indexMap[t];
			if (idx !== undefined) {
				v[idx] += weight * tfidf(t, stats);
			}
		}
	};
	addTerms(movie.genres, 3); // Adjust weight
	addTerms(movie.keywords, 1);
	addTerms(movie.cast_names, 2);
	addTerms(movie.director_names, 3);
	normalize(v);
	return v;
}

export function profileToVector(
	prefs: UserPrefsRaw,
	stats: TfIdfStats,
	indexMap: Record<string, number>,
	totalDim: number
): Vector {
	const v = new Float32Array(totalDim);
	const addMap = (map: Record<string, number>, weight: number) => {
		for (const [term, score] of Object.entries(map)) {
			const idx = indexMap[term];
			if (idx !== undefined && score !== 0) {
				v[idx] += score * weight * tfidf(term, stats);
			}
		}
	};
	addMap(prefs.genres, 3); // Adjust weight
	addMap(prefs.keywords, 1);
	addMap(prefs.actors, 2);
	addMap(prefs.directors, 3);
	normalize(v);
	return v;
}

export function scoreAllMovies(
	userVec: Vector,
	movieVectors: Record<string, Vector>
): { movieId: string; score: number }[] {
	const out: { movieId: string; score: number }[] = [];
	for (const [id, mvec] of Object.entries(movieVectors)) {
		out.push({ movieId: id, score: cosine(userVec, mvec) });
	}
	return out;
}
