<script lang="ts">
	import Landing from '$lib/components/pages/landing.svelte';
	import Feed from '$lib/components/pages/feed.svelte';

	export let data; // Data passed from the server

	// Destructure session and movies from the server's data
	let { session, movies, supabase } = data;
</script>

<svelte:head>
	<title>Original Cinema</title>
</svelte:head>

{#if !session}
	<!-- Show the Landing page when no session (user not logged in) -->
	<Landing />
{:else}
	<!-- Pass the movies data to the Feed component when session exists -->
	<Feed {movies} {supabase} />
{/if}
