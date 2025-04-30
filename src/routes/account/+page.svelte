<script lang="ts">
	import { onMount, tick } from 'svelte';
	import { browser } from '$app/environment';
	import { Motion } from 'svelte-motion'; // Corrected import for svelte-motion

	import CircleUser from 'lucide-svelte/icons/circle-user';
	import Menu from 'lucide-svelte/icons/menu';
	import Package2 from 'lucide-svelte/icons/package-2';
	import Search from 'lucide-svelte/icons/search';

	import { Chart, registerables, type ChartData } from 'chart.js';

	import { Button } from '$lib/components/ui/button';
	import * as Card from '$lib/components/ui/card';
	import { Input } from '$lib/components/ui/input';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu';
	import * as Sheet from '$lib/components/ui/sheet';
	import type { SupabaseClient } from '@supabase/supabase-js';

	Chart.register(...registerables);

	export let data;

	let { session, supabase } = data;

	let chartInstance: Chart | null = null;
	let selectedAnalyticsTab = 'Genres';
	let mounted = false;

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

	let chartData: Record<string, Record<string, number>> = { genres: {}, keywords: {}, actors: {}, directors: {} };

	async function loadChartData() {
		try {
			const preferences = await fetchUserPreferences(supabase, session.user.id);
			chartData = {
				genres: preferences.genres,
				keywords: preferences.keywords,
				actors: preferences.actors,
				directors: preferences.directors
			};
		} catch (error) {
			console.error('Error fetching user preferences:', error);
		}
	}

	onMount(() => {
		loadChartData();
	});

	function renderChart(canvas: HTMLCanvasElement) {
		if (!canvas) return;
		if (chartInstance) chartInstance.destroy();

		const key = selectedAnalyticsTab.toLowerCase() as keyof typeof chartData;
		const entries = Object.entries(chartData[key]).sort((a, b) => b[1] - a[1]);

		chartInstance = new Chart(canvas, {
			type: 'bar',
			data: {
				labels: entries.map(([name]) => name),
				datasets: [
					{
						label: selectedAnalyticsTab,
						data: entries.map(([_, score]) => score) as (number | null)[],
						backgroundColor: 'hsl(var(--primary) / 0.7)',
						borderRadius: 8
					}
				]
			} as ChartData<'bar', (number | null)[], string>,
			options: {
				responsive: true,
				plugins: { legend: { display: false } },
				scales: {
					x: { grid: { display: false } },
					y: { beginAtZero: true }
				}
			}
		});
	}

	$: if (browser && mounted && selectedAnalyticsTab) {
		tick().then(() => {
			const canvas = document.getElementById('chart-canvas') as HTMLCanvasElement;
			if (canvas) renderChart(canvas);
		});
	}

	onMount(() => {
		mounted = true;
	});

	const analyticsTabs = ['Genres', 'Actors', 'Keywords', 'Directors'];
</script>

<div class="flex min-h-screen w-full flex-col">
	<!-- HEADER -->
	<header class="bg-background sticky top-0 flex h-16 items-center gap-4 border-b px-4 md:px-6">
		<nav
			class="hidden flex-col gap-6 text-lg font-medium md:flex md:flex-row md:items-center md:gap-5 md:text-sm lg:gap-6"
		>
			<a href="##" class="flex items-center gap-2 text-lg font-semibold md:text-base">
				<Package2 class="h-6 w-6" />
				<span class="sr-only">Acme Inc</span>
			</a>
			<a href="##" class="text-muted-foreground hover:text-foreground transition-colors">
				Dashboard
			</a>
			<a href="##" class="text-muted-foreground hover:text-foreground transition-colors">
				Orders
			</a>
			<a href="##" class="text-muted-foreground hover:text-foreground transition-colors">
				Products
			</a>
			<a href="##" class="text-muted-foreground hover:text-foreground transition-colors">
				Customers
			</a>
			<a href="##" class="text-foreground hover:text-foreground transition-colors"> Settings </a>
		</nav>
		<Sheet.Root>
			<Sheet.Trigger asChild let:builder>
				<Button variant="outline" size="icon" class="shrink-0 md:hidden" builders={[builder]}>
					<Menu class="h-5 w-5" />
					<span class="sr-only">Toggle navigation menu</span>
				</Button>
			</Sheet.Trigger>
			<Sheet.Content side="left">
				<nav class="grid gap-6 text-lg font-medium">
					<a href="##" class="flex items-center gap-2 text-lg font-semibold">
						<Package2 class="h-6 w-6" />
						<span class="sr-only">Acme Inc</span>
					</a>
					<a href="##" class="text-muted-foreground hover:text-foreground"> Dashboard </a>
					<a href="##" class="text-muted-foreground hover:text-foreground"> Orders </a>
					<a href="##" class="text-muted-foreground hover:text-foreground"> Products </a>
					<a href="##" class="text-muted-foreground hover:text-foreground"> Customers </a>
					<a href="##" class="hover:text-foreground"> Settings </a>
				</nav>
			</Sheet.Content>
		</Sheet.Root>
		<div class="flex w-full items-center gap-4 md:ml-auto md:gap-2 lg:gap-4">
			<form class="ml-auto flex-1 sm:flex-initial">
				<div class="relative">
					<Search class="text-muted-foreground absolute top-2.5 left-2.5 h-4 w-4" />
					<Input
						type="search"
						placeholder="Search products..."
						class="pl-8 sm:w-[300px] md:w-[200px] lg:w-[300px]"
					/>
				</div>
			</form>
			<DropdownMenu.Root>
				<DropdownMenu.Trigger asChild let:builder>
					<Button builders={[builder]} variant="secondary" size="icon" class="rounded-full">
						<CircleUser class="h-5 w-5" />
						<span class="sr-only">Toggle user menu</span>
					</Button>
				</DropdownMenu.Trigger>
				<DropdownMenu.Content align="end">
					<DropdownMenu.Label>My Account</DropdownMenu.Label>
					<DropdownMenu.Separator />
					<DropdownMenu.Item>Settings</DropdownMenu.Item>
					<DropdownMenu.Item>Support</DropdownMenu.Item>
					<DropdownMenu.Separator />
					<DropdownMenu.Item>Logout</DropdownMenu.Item>
				</DropdownMenu.Content>
			</DropdownMenu.Root>
		</div>
	</header>

	<!-- MAIN -->
	<main
		class="bg-muted/40 flex min-h-[calc(100vh_-_theme(spacing.16))] flex-1 flex-col gap-4 p-4 md:gap-8 md:p-10"
	>
		<div class="mx-auto grid w-full max-w-6xl gap-2">
			<h1 class="text-foreground text-3xl font-semibold">Analytics</h1>
		</div>

		<div class="mx-auto grid w-full max-w-6xl gap-6">
			<!-- Tabs with motion -->
			<div class="relative flex space-x-4 overflow-x-auto pb-2">
				{#each analyticsTabs as tab}
					<Button variant="ghost" on:click={() => (selectedAnalyticsTab = tab)} class="relative">
						{tab}
						{#if tab === selectedAnalyticsTab}
							<Motion
								animate={{ scale: 1.1 }}
								transition={{ type: 'spring', stiffness: 300 }}
								style="background-color: var(--primary); position: absolute; bottom: -2px; left: 0; right: 0; height: 2px; border-radius: 50%;"
							/>
						{/if}
					</Button>
				{/each}
			</div>

			<!-- Chart -->
			<div class="bg-background rounded-2xl p-6 shadow-lg">
				<canvas id="chart-canvas" class="h-80 w-full" />
			</div>
		</div>
	</main>
</div>
