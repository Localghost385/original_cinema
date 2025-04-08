<!-- src/routes/+page.svelte -->
<script lang="ts">
	import Landing from '$lib/components/pages/landing.svelte';
	import Feed from '$lib/components/pages/feed.svelte';
	export let data;
</script>

<svelte:head>
	<title>Cinematch</title>
</svelte:head>

{#if !data.session}
	<Landing />
{:else}
	<Feed />
{/if}
