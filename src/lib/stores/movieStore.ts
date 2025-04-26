import { writable } from 'svelte/store';
import type { Movie } from '$lib/types';

export const currentMovies = writable<Movie[]>([]);
export const seenMovies = writable<Set<string>>(new Set());
export const currentIndex = writable<number>(0);
