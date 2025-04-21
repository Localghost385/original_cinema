<!-- src/routes/+page.svelte -->
<script lang="ts">
	import Landing from '$lib/components/pages/landing.svelte';
	import Feed from '$lib/components/pages/feed.svelte';
	export let data;

	const movies = [
		{
			title: 'Dune',
			year: '2021',
			poster: 'https://image.tmdb.org/t/p/w500/d5NXSklXo0qyIYkgV94XAgMIckC.jpg',
			description:
				"A noble family becomes embroiled in a war for control over the galaxy's most valuable asset.",
			genres: ['Science Fiction', 'Adventure'],
			actors: ['Timothée Chalamet', 'Rebecca Ferguson', 'Oscar Isaac'],
			director: 'Denis Villeneuve'
		},
		{
			title: 'La La Land',
			year: '2016',
			poster: 'https://image.tmdb.org/t/p/w500/uDO8zWDhfWwoFdKS4fzkUJt0Rf0.jpg',
			description:
				'An aspiring actress and a jazz musician pursue their dreams in Los Angeles, facing love and heartbreak.',
			genres: ['Romance', 'Drama', 'Musical'],
			actors: ['Emma Stone', 'Ryan Gosling'],
			director: 'Damien Chazelle'
		},
		{
			title: 'The Batman',
			year: '2022',
			poster: 'https://image.tmdb.org/t/p/w500/74xTEgt7R36Fpooo50r9T25onhq.jpg',
			description:
				'Batman uncovers corruption in Gotham City that connects to his own family while facing the Riddler.',
			genres: ['Action', 'Mystery', 'Crime'],
			actors: ['Robert Pattinson', 'Zoë Kravitz', 'Paul Dano'],
			director: 'Matt Reeves'
		},
		{
			title: 'Everything Everywhere All at Once',
			year: '2022',
			poster: 'https://image.tmdb.org/t/p/w500/w3LxiVYdWWRvEVdn5RYq6jIqkb1.jpg',
			description:
				'An unlikely hero must channel her newfound powers to save the multiverse from a mysterious force.',
			genres: ['Comedy', 'Action', 'Sci-Fi'],
			actors: ['Michelle Yeoh', 'Stephanie Hsu', 'Ke Huy Quan'],
			director: 'Daniel Kwan & Daniel Scheinert'
		},
		{
			title: 'The Grand Budapest Hotel',
			year: '2014',
			poster: 'https://image.tmdb.org/t/p/w500/nX5XotM9yprCKarRH4fzOq1VM1J.jpg',
			description:
				'A whimsical tale of a legendary concierge at a famous hotel and his young protégé.',
			genres: ['Comedy', 'Drama', 'Crime'],
			actors: ['Ralph Fiennes', 'Tony Revolori', 'Saoirse Ronan'],
			director: 'Wes Anderson'
		}
	];
</script>

<svelte:head>
	<title>Cinematch</title>
</svelte:head>

{#if !data.session}
	<Landing />
{:else}
	<Feed {movies} />
{/if}
