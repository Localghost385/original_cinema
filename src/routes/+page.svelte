<script lang="ts">
	import Landing from '$lib/components/pages/landing.svelte';
	import Feed from '$lib/components/pages/feed.svelte';
	import type { SupabaseClient } from '@supabase/supabase-js';

	const fetchUserPreferences = async (supabase: SupabaseClient, user_id: string) => {
		const { data, error } = await supabase
			.from('user_preferences_cache')
			.select('*')
			.eq('profile_id', user_id)
			.single();

		if (error || !data) {
			throw new Error('User preferences not found');
		}

		console.log(data);

		return {
			genres: data.genres || {},
			keywords: data.keywords || {},
			actors: data.actors || {},
			directors: data.directors || {}
		};
	};
	export let data; // Data passed from the server


	let { session, movies, supabase } = data;

	if (session?.user.id) {
		fetchUserPreferences(supabase, session.user.id)
			.then((preferences) => {
				console.log('User preferences:', preferences);
			})
			.catch((error) => {
				console.error('Error fetching user preferences:', error);
			});
	} else {
		console.error('User ID is undefined');
	}

	// Destructure session and movies from the server's data
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


