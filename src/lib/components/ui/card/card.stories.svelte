<script module>
	import { defineMeta } from '@storybook/addon-svelte-csf';
	import * as Card from '$lib/components/ui/card';

	const { Story } = defineMeta({
		component: Card.Root,
		title: 'ShadCN/Card'
	});
</script>

<Story name="primary" args={{}}>
	<Card.Root>
		<Card.Header>
			<Card.Title>Card Title</Card.Title>
			<Card.Description>Card Description</Card.Description>
		</Card.Header>
		<Card.Content>
			<p>Card Content</p>
		</Card.Content>
		<Card.Footer>
			<p>Card Footer</p>
		</Card.Footer>
	</Card.Root>
</Story>
