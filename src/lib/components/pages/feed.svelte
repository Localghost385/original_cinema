<script lang="ts">
	import { onMount, tick } from 'svelte';
	import MovieCard from '$lib/components/ui/movie_card/movieCard.svelte';
	import type { SupabaseClient } from '@supabase/supabase-js';

	export let movies: Array<{
		title: string;
		year: string;
		poster: string;
		description: string;
		genres: string[];
		actors: string[];
		director: string;
		movie_id: string;
		score: number;
	}> = [];

	//eslint-disable-next-line @typescript-eslint/@typescript-eslint/no-explicit-any
	export let supabase: SupabaseClient<any, 'public', any>;

	let current = 0;
	let loading = false;
	let scrolling = false;
	let cardRefs: HTMLElement[] = [];

	function scrollToCurrentCard() {
		const el = cardRefs[current];
		if (el) {
			el.scrollIntoView({ behavior: 'smooth' });
		}
	}

	function nextMovie() {
		if (current < movies.length - 1) {
			current += 1;
			scrollToCurrentCard();
		} else {
			loadMoreMovies();
		}
	}

	function prevMovie() {
		if (current > 0) {
			current -= 1;
			scrollToCurrentCard();
		}
	}

	function onScroll(e: WheelEvent) {
		if (scrolling || loading) return;
		scrolling = true;

		if (e.deltaY > 50) nextMovie();
		else if (e.deltaY < -50) prevMovie();

		setTimeout(() => (scrolling = false), 400);
	}

	// Function to load more movies
	function loadMoreMovies() {
		if (loading) return;
		loading = true;
	}

	function setCardRef(el: HTMLElement, index: number) {
		cardRefs[index] = el;
	}

	// Scroll to the current movie card after the page renders
	$: if (!loading) {
		tick().then(() => {
			setTimeout(() => {
				scrollToCurrentCard();
			}, 50); // Give the browser a little breathing room
		});
	}

	// Handle keyboard navigation
	onMount(() => {
		window.addEventListener('keydown', (e) => {
			if (e.key === 'ArrowDown') nextMovie();
			else if (e.key === 'ArrowUp') prevMovie();
		});
	});
</script>

<div
	class="card-container relative h-[calc(100vh-64px)] snap-y snap-mandatory overflow-y-scroll"
	on:wheel={onScroll}
>
	{#each movies as movie, index}
		<div
			class="flex h-[calc(100vh-64px)] snap-start items-center justify-center"
			use:setCardRef={index}
		>
			<MovieCard {...movie} {supabase} />
		</div>
	{/each}
</div>

<style>
	.card-container::-webkit-scrollbar {
		display: none;
	}
</style>
