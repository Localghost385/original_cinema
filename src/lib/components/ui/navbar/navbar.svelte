<script lang="ts">
	import Light from '$lib/components/ui/light_switch/light_switch.svelte';
	import { Button } from '$lib/components/ui/button';
	import type { Session, SupabaseClient } from '@supabase/supabase-js';

	export let data: { supabase: SupabaseClient<any, 'public', any>; session: Session | null };
</script>

<div
	class="bg-background bg-opacity-70 border-border sticky top-0 z-50 flex h-14 w-full flex-row items-center justify-between border-b-[1px] pr-[10vw] pl-[10vw] backdrop-blur"
>
	<div class=" flex flex-row items-center justify-evenly">
		<svg class="h-10 w-10" width="100" height="100" viewBox="0 0 26.458333 26.458333">
			<path
				style="fill:none;stroke:#000000cc;stroke-width:1.75;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers"
				d="M 13.419335,18.520833 19.362709,13.229167 13.419335,7.9374997"
				id="path1"
				class="bg-red-500"
			/>
			<path
				style="fill:none;stroke:#000000cc;stroke-width:1.75;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:none;stroke-opacity:1;paint-order:stroke fill markers"
				d="M 9.4506231,18.520833 V 7.9374997"
				id="path2"
			/>
		</svg>

		<Button variant="link" href="/" class="text-md px-1 font-semibold">original cinema</Button>
	</div>
	<div class=" flex flex-row items-center justify-evenly">
		{#if data.session}
			<Button variant="link" href="/account">analytics</Button>
		{:else}
			<Button variant="link" href="/login">Login</Button>
		{/if}
		<Light />
	</div>
</div>
