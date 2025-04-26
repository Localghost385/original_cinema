<script lang="ts">
	export let title: string;
	export let year: string;
	export let poster: string;
	export let description: string;
	export let genres: string[] = [];
	export let actors: string[] = [];
	export let director: string;
	export let movie_id: string; // Add movie UUID to identify the movie
	export let score: number;
	export let supabase: SupabaseClient<any, 'public', any>;

	import { Button } from '$lib/components/ui/button/index.js';
	import { onMount } from 'svelte';
	import { Badge } from '$lib/components/ui/badge/index.js';
	import { ThumbsUp, ThumbsDown, Bookmark, X } from 'lucide-svelte';
	import type { SupabaseClient } from '@supabase/supabase-js';

	let showFullDescription = false;

	const toggleDescription = () => {
		if (window.innerWidth < 1024) {
			showFullDescription = !showFullDescription;
		}
	};

	onMount(() => {
		if (window.innerWidth > 1024) {
			showFullDescription = true;
		}
	});

	async function interact(action: 'like' | 'dislike' | 'watchlist' | 'not_interested') {
		const {
			data: { user },
			error: userError
		} = await supabase.auth.getUser();

		if (userError || !user) return console.error('User not authenticated');

		const profileId = user.id;

		if (!movie_id) {
			console.error('Movie ID is missing');
			return;
		}

		try {
			let interactionUpdate;
			let request = {
				profile_id: profileId,
				movie_id: movie_id, // Ensure movieId is properly assigned
				preference_type: action
			};

			console.log(request);

			// Insert the interaction into the user_movie_preferences table
			interactionUpdate = await supabase.from('user_movie_preferences').insert([request]);

			if (interactionUpdate.error) {
				console.error('Failed to insert interaction:', interactionUpdate.error.message);
			} else {
				console.log('Successfully inserted interaction');
			}
		} catch (err) {
			console.error('Interaction failed:', err);
		}
	}

	async function updatePreferencesCache(profileId: string) {
		// Call a function that will update the preferences cache for the user
		// Assuming you have a function like this in your backend or Supabase function
		const { error } = await supabase.rpc('update_preferences_cache', { profile_id: profileId });

		if (error) {
			console.error('Failed to update preferences cache:', error);
		} else {
			console.log('Preferences cache updated');
		}
	}
</script>

<!-- Updated `movieCard.svelte` -->
<div class="relative h-[calc(100vh-64px)] w-full overflow-hidden">
	<!-- MOBILE Poster -->
	<div class="absolute inset-0 lg:hidden">
		<img src={poster} alt={`Poster for ${title}`} class="h-full w-full object-cover" />
		<div
			class="from-background via-background/60 absolute inset-0 bg-gradient-to-t to-transparent"
		></div>
	</div>

	<div
		class="relative z-10 flex h-full w-full flex-col justify-end lg:flex-row lg:justify-normal lg:p-12"
	>
		<!-- DESKTOP Poster -->
		<div class="hidden w-2/5 items-center justify-center lg:flex">
			<img
				src={poster}
				alt={`Poster for ${title}`}
				class="max-h-[90%] rounded-xl object-cover shadow-lg"
			/>
		</div>

		<!-- Info Panel -->
		<div
			class="mt-auto flex w-full flex-col justify-between p-6 lg:mt-0 lg:w-3/5 lg:bg-transparent lg:px-10 lg:py-6"
		>
			<div class="lg:mb-auto">
				<h1 class="text-4xl font-bold drop-shadow">
					{title}<span class="text-muted-foreground text-2xl font-normal">({year})</span>
				</h1>
				<p
					class="text-muted-foreground mt-4 max-w-2xl cursor-pointer text-base text-balance transition-all duration-300 lg:cursor-default"
					class:line-clamp-2={!showFullDescription}
					on:click={toggleDescription}
				>
					{description}
				</p>

				<div class="mt-4 flex flex-wrap gap-2">
					{#each genres as genre}
						<Badge>{genre}</Badge>
					{/each}
				</div>

				<div class="text-muted-foreground mt-6 hidden space-y-1 text-sm lg:block">
					<p><span class="font-semibold">Starring:</span> {actors.join(', ')}</p>
					<p><span class="font-semibold">Director:</span> {director}</p>
				</div>
			</div>

			<div class="mt-6 flex gap-4 lg:mt-0">
				<Button size="icon" on:click={() => interact('like')}><ThumbsUp class="h-5 w-5" /></Button>
				<Button size="icon" on:click={() => interact('dislike')}
					><ThumbsDown class="h-5 w-5" /></Button
				>
				<Button variant="outline" size="icon" on:click={() => interact('watchlist')}
					><Bookmark class="h-5 w-5" /></Button
				>
				<Button variant="outline" size="icon" on:click={() => interact('not_interested')}
					><X class="h-5 w-5" /></Button
				>
				{score}
			</div>
		</div>
	</div>
</div>

<style>
	.line-clamp-2 {
		display: -webkit-box;
		-webkit-line-clamp: 2;
		-webkit-box-orient: vertical;
		overflow: hidden;
	}
</style>
