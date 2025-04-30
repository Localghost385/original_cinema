<!-- src/routes/+layout.svelte -->
<script lang="ts">
	import { invalidate } from '$app/navigation';
	import { onMount } from 'svelte';

	import Navbar from '$lib/components/ui/navbar/navbar.svelte';

	import { ModeWatcher } from 'mode-watcher';

	import '../app.css';

	export let data;

	let { supabase, session } = data;
	$: ({ supabase, session } = data);

	onMount(() => {
		const { data } = supabase.auth.onAuthStateChange((event, newSession) => {
			if (newSession?.expires_at !== session?.expires_at) {
				invalidate('supabase:auth');
			}
		});

		return () => data.subscription.unsubscribe();
	});
</script>

<svelte:head>
	<title>User Management</title>
</svelte:head>

<ModeWatcher />
<Navbar {data} />

<div class="h-full w-full">
	<slot />
</div>
