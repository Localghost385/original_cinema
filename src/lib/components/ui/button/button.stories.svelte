<script module>
	import { defineMeta } from '@storybook/addon-svelte-csf';
	import Button from '$lib/components/ui/button/button.svelte';

	const { Story } = defineMeta({
		component: Button,
		title: 'ShadCN/Button',
		argTypes: {
			variant: {
				control: 'select',
				options: ['default', 'secondary', 'destructive', 'outline', 'ghost', 'link']
			},
			size: {
				control: 'select',
				options: ['default', 'sm', 'lg', 'icon']
			},
			disabled: {
				control: 'boolean'
			}
		}
	});
</script>

<Story name="primary" args={{ variant: 'default', size: 'default', disabled: false }}>
	{#snippet children(/** @type {any} */ args)}
		<Button {...args}>Click Me</Button>
	{/snippet}
</Story>

<Story name="secondary" args={{ variant: 'secondary', size: 'default', disabled: false }}>
	{#snippet children(/** @type {any} */ args)}
		<Button {...args}>Click Me</Button>
	{/snippet}
</Story>

<Story name="Destructive" args={{ variant: 'destructive', size: 'default' }}>
	{#snippet children(/** @type {any} */ args)}
		<Button {...args}>Click Me</Button>
	{/snippet}
</Story>

<Story name="Outline" args={{ variant: 'outline', size: 'default' }}>
	{#snippet children(/** @type {any} */ args)}
		<Button {...args}>Click Me</Button>
	{/snippet}
</Story>

<Story name="ghost" args={{ variant: 'ghost', size: 'default' }}>
	{#snippet children(/** @type {any} */ args)}
		<Button {...args}>Click Me</Button>
	{/snippet}
</Story>

<Story name="link" args={{ variant: 'link', size: 'default' }}>
	{#snippet children(/** @type {any} */ args)}
		<Button {...args}>Click Me</Button>
	{/snippet}
</Story>

<Story name="Disabled" args={{ variant: 'default', size: 'default', disabled: true }}>
	{#snippet children(/** @type {any} */ args)}
		<Button disabled {...args}>Click Me</Button>
	{/snippet}
</Story>
