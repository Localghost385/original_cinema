<script lang="ts">
	export let width = '100%';
	export let height = '20px';
</script>

<div class="relative h-[calc(100vh-64px)] w-full overflow-hidden">
	<!-- MOBILE Poster Skeleton -->
	<div class="absolute inset-0 lg:hidden">
		<div class="skeleton h-full w-full object-cover"></div>
		<div class="from-background via-background/60 absolute inset-0 bg-gradient-to-t to-transparent"></div>
	</div>

	<div class="relative z-10 flex h-full w-full flex-col justify-end lg:flex-row lg:justify-normal lg:p-12">
		<!-- DESKTOP Poster Skeleton -->
		<div class="hidden w-2/5 items-center justify-center lg:flex">
			<div class="flex h-[90%] w-full items-center justify-center">
				<div class="skeleton h-[100%] w-[67.5%] rounded-xl object-cover shadow-lg"></div>
			</div>
		</div>

		<!-- Info Panel Skeleton -->
		<div class="mt-auto flex w-full flex-col justify-between p-6 lg:mt-0 lg:w-3/5 lg:bg-transparent lg:px-10 lg:py-6">
			<div class="lg:mb-auto space-y-6">
				<!-- Title Skeleton -->
				<div class="skeleton h-10 w-2/3"></div>

				<!-- Description Skeleton -->
				<div class="space-y-3 mt-4">
					<div class="skeleton h-4 w-full"></div>
					<div class="skeleton h-4 w-5/6"></div>
				</div>

				<!-- Genres Skeleton -->
				<div class="mt-6 flex flex-wrap gap-2">
					<div class="skeleton h-6 w-20 rounded-full"></div>
					<div class="skeleton h-6 w-16 rounded-full"></div>
					<div class="skeleton h-6 w-24 rounded-full"></div>
				</div>

				<!-- Actors/Director Skeleton -->
				<div class="text-muted-foreground mt-8 hidden space-y-3 text-sm lg:block">
					<div class="skeleton h-4 w-3/5"></div>
					<div class="skeleton h-4 w-2/5"></div>
				</div>
			</div>

			<!-- Buttons Skeleton -->
			<div class="mt-8 flex gap-4 lg:mt-0">
				<div class="skeleton h-10 w-10 rounded-full"></div>
				<div class="skeleton h-10 w-10 rounded-full"></div>
				<div class="skeleton h-10 w-10 rounded-full"></div>
				<div class="skeleton h-10 w-10 rounded-full"></div>
			</div>
		</div>
	</div>
</div>

<style>
	.skeleton {
		background: linear-gradient(60deg, #e0e0e0 25%, #f0f0f0 50%, #e0e0e0 75%);
		background-size: 200% 100%;
		animation: shimmer 2.5s infinite;
		border-radius: 4px;
	}

	@keyframes shimmer {
		0% {
			background-position: 200% 0;
		}
		100% {
			background-position: -200% 0;
		}
	}
</style>
