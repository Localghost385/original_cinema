<script lang="ts">
	import { Button } from '$lib/components/ui/button/index.js';
	import * as Card from '$lib/components/ui/card/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	import { enhance } from '$app/forms';
	import type { ActionData, SubmitFunction } from './$types.js';

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
	<Card.Root class="mx-auto max-w-sm">
		<Card.Header>
			<Card.Title class="text-xl">Sign Up</Card.Title>
			<Card.Description>Enter your information to create an account</Card.Description>
		</Card.Header>
		<Card.Content>
			<form class="grid gap-4" method="POST" use:enhance={handleSubmit}>
				{#if form?.message !== undefined}
					<div class="success {form?.success ? '' : 'fail'}">{form?.message}</div>
				{/if}
				<div class="grid grid-cols-2 gap-4">
					<div class="grid gap-2">
						<Label for="first-name">First name</Label>
						<Input id="first-name" name="first_name" placeholder="Max" required />
					</div>
					<div class="grid gap-2">
						<Label for="last-name">Last name</Label>
						<Input id="last-name" name="last_name" placeholder="Robinson" required />
					</div>
				</div>
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
					<Label for="password">Password</Label>
					<Input id="password" name="password" type="password" required />
				</div>
				<Button type="submit" class="w-full" disabled={loading}
					>{loading ? 'Creating account...' : 'Create an account'}</Button
				>
			</form>
			<div class="mt-4 text-center text-sm">
				Already have an account? <a href="login" class="underline"> Sign in </a>
			</div>
		</Card.Content>
	</Card.Root>
</div>
