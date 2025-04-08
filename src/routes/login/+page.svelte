<script lang="ts">
	import { Button } from '$lib/components/ui/button/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	import { enhance } from '$app/forms';
	import type { ActionData, SubmitFunction } from './$types.js';

	import LoaderCircle from 'lucide-svelte/icons/loader-circle';

	export let form: ActionData;

	let loading = false;

	const handleSubmit: SubmitFunction = () => {
		loading = true;
		return async ({ update }) => {
			update();
			loading = false;
		};
	};
</script>

<div class="flex h-[calc(100vh-64px)] flex-col justify-evenly">
	<div
		class="w-full lg:grid lg:min-h-[calc(100vh-64px)] lg:grid-cols-2 xl:min-h-[calc(100vh-64px)]"
	>
		<div class="flex items-center justify-center py-12">
			<div class="mx-auto grid w-[350px] gap-6">
				<div class="grid gap-2 text-center">
					<h1 class="text-3xl font-bold">Login</h1>
					<p class="text-muted-foreground text-balance">
						Enter your email below to login to your account
					</p>
				</div>
				<form class="grid gap-4" method="POST" use:enhance={handleSubmit}>
					{#if form?.message !== undefined}
						<div class="success {form?.success ? '' : 'fail'}">{form?.message}</div>
					{/if}
					<div class="grid gap-2">
						<Label for="email">Email</Label>
						<Input
							id="email"
							name="email"
							type="email"
							placeholder="m@example.com"
							required
							value={form?.email ?? ''}
						/>
					</div>
					{#if form?.errors?.email}
						<span class="error text-sm">{form?.errors?.email}</span>
					{/if}
					<div class="grid gap-2">
						<div class="flex items-center">
							<Label for="password">Password</Label>
							<a href="##" class="ml-auto inline-block text-sm underline">Forgot your password?</a>
						</div>
						<Input id="password" name="password" type="password" required />
					</div>
					<Button type="submit" class="w-full" disabled={loading}>
						{#if loading}
							<LoaderCircle class="mr-2 h-4 w-4 animate-spin" />
						{/if}
						{loading ? 'Loading...' : 'Login'}
					</Button>
				</form>
				<div class="mt-4 text-center text-sm">
					Don't have an account? <a href="/sign_up" class="underline"> Sign up </a>
				</div>
			</div>
		</div>
		<div class="bg-muted hidden lg:block">
			<img
				src="/images/placeholder.svg"
				alt="placeholder"
				width="1920"
				height="1080"
				class="h-full w-full object-cover dark:brightness-[0.2] dark:grayscale"
			/>
		</div>
	</div>
</div>
