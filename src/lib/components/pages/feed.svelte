<script lang="ts">
	import { onMount, tick } from 'svelte';
	import MovieCard from '$lib/components/ui/movie_card/movieCard.svelte';

	let movies = [
		{
			title: 'Dune',
			year: '2021',
			poster: 'https://image.tmdb.org/t/p/w500/8r1tuYS10k0CZ9j5Y56kGkD9FqV.jpg',
			description:
				"A noble family becomes embroiled in a war for control of the galaxy's most valuable asset while its heir becomes troubled by visions of a dark future.",
			genres: ['Action', 'Adventure', 'Sci-Fi'],
			actors: ['Timothée Chalamet', 'Rebecca Ferguson', 'Oscar Isaac'],
			director: 'Denis Villeneuve'
		},
		{
			title: 'La La Land',
			year: '2016',
			poster: 'https://image.tmdb.org/t/p/w500/4Y7G2IFv7IWfVO8l8tcDlnhgprj.jpg',
			description:
				'While navigating their careers in Los Angeles, a jazz musician and an aspiring actress fall in love but struggle to maintain their relationship as they become more successful.',
			genres: ['Drama', 'Music', 'Romance'],
			actors: ['Ryan Gosling', 'Emma Stone', 'John Legend'],
			director: 'Damien Chazelle'
		},
		{
			title: 'Everything Everywhere All at Once',
			year: '2022',
			poster: 'https://image.tmdb.org/t/p/w500/tl1M8yRKLHgUGLwvMGjsXgX2pft.jpg',
			description:
				'An aging Chinese immigrant is swept up in an insane adventure, where she alone can save the world by exploring other universes connecting with the lives she could have led.',
			genres: ['Action', 'Adventure', 'Comedy'],
			actors: ['Michelle Yeoh', 'Ke Huy Quan', 'Stephanie Hsu'],
			director: 'Daniel Kwan, Daniel Scheinert'
		},
		{
			title: 'Inception',
			year: '2010',
			poster: 'https://image.tmdb.org/t/p/w500/5kqI0lbIR3tH5ty3fEd0HaSmyA7.jpg',
			description:
				'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO.',
			genres: ['Action', 'Adventure', 'Sci-Fi'],
			actors: ['Leonardo DiCaprio', 'Joseph Gordon-Levitt', 'Ellen Page'],
			director: 'Christopher Nolan'
		},
		{
			title: 'The Matrix',
			year: '1999',
			poster: 'https://image.tmdb.org/t/p/w500/dvczdIkAK77TfaP6tgpJH4vNS1z.jpg',
			description:
				'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.',
			genres: ['Action', 'Sci-Fi'],
			actors: ['Keanu Reeves', 'Laurence Fishburne', 'Carrie-Anne Moss'],
			director: 'The Wachowskis'
		}
		// Add more movies as needed...
	];
	let current = 0;
	let loading = false;
	let scrolling = false;

	let cardRefs: HTMLElement[] = [];

	function scrollToCurrentCard() {
		const el = cardRefs[current];
		if (el) {
			el.scrollIntoView({ behavior: 'smooth' });
		}
	}

	function nextMovie() {
		if (current < movies.length - 1) {
			current += 1;
			scrollToCurrentCard();
		} else {
			loadMoreMovies();
		}
	}

	function prevMovie() {
		if (current > 0) {
			current -= 1;
			scrollToCurrentCard();
		}
	}

	function onScroll(e: WheelEvent) {
		if (scrolling || loading) return;
		scrolling = true;

		if (e.deltaY > 50) nextMovie();
		else if (e.deltaY < -50) prevMovie();

		setTimeout(() => (scrolling = false), 400);
	}

	function loadMoreMovies() {
		if (loading) return;
		loading = true;
		setTimeout(() => {
			movies = [
				...movies,
				{
					title: `Generated Movie ${movies.length + 1}`,
					year: '2024',
					poster: 'https://image.tmdb.org/t/p/w500/example.jpg',
					description: 'Just another one.',
					genres: ['Drama'],
					actors: ['Actor X'],
					director: 'A Director'
				}
			];
			loading = false;
		}, 50);
	}

	function setCardRef(el: HTMLElement, index: number) {
		cardRefs[index] = el;
	}

	$: if (!loading) {
		tick().then(() => {
			setTimeout(() => {
				scrollToCurrentCard();
			}, 50); // Give browser a little breathing room
		});
	}

	onMount(() => {
		window.addEventListener('keydown', (e) => {
			if (e.key === 'ArrowDown') nextMovie();
			else if (e.key === 'ArrowUp') prevMovie();
		});
	});
</script>

<div
	class="card-container relative h-[calc(100vh-64px)] snap-y snap-mandatory overflow-y-scroll"
	on:wheel={onScroll}
>
	{#each movies as movie, index}
		<div
			class="flex h-[calc(100vh-64px)] snap-start items-center justify-center"
			use:setCardRef={index}
		>
			<MovieCard {...movie} />
		</div>
	{/each}
</div>

<style>
	.card-container::-webkit-scrollbar {
		display: none;
	}
</style>
