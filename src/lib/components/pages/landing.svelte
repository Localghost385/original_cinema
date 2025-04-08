<script lang="ts">
	import { Button } from '$lib/components/ui/button';
</script>

<div
	class="flex h-[calc(100vh-64px)] flex-col justify-evenly bg-[url('/src/lib/images/wiggle_light.svg')] bg-cover bg-center bg-no-repeat dark:bg-[url('/src/lib/images/wiggle_dark.svg')]"
>
	<div
		class="w-full lg:grid lg:min-h-[calc(100vh-64px)] lg:grid-cols-2 xl:min-h-[calc(100vh-64px)]"
	>
		<div class="flex items-center justify-center py-12">
			<div class="mx-auto grid w-[500px] gap-6">
				<div class="grid gap-2 text-left">
					<h1 class="w-[350px] text-3xl font-bold">Discover Your new favorite movies.</h1>
					<p class="text-muted-foreground text-balance">
						Log in or sign up to get personalized movie recommendations, track what you've watched,
						and discover your next favorite film.
					</p>
					<div class="my-2">
						<Button variant="outline" href="/login">Get Started Now</Button>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
