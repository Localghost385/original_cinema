<script lang="ts">
    export let title: string;
    export let year: string;
    export let poster: string;
    export let description: string;
    export let genres: string[] = [];
    export let actors: string[] = [];
    export let director: string;
  
    import { Button } from '$lib/components/ui/button/index.js';
    import { Badge } from '$lib/components/ui/badge/index.js';
    import { ThumbsUp, ThumbsDown, Bookmark, X } from 'lucide-svelte';
  
    let showFullDescription = false;
  
    const toggleDescription = () => {
      if (window.innerWidth < 1024) {
        showFullDescription = !showFullDescription;
      }
    };
  </script>
  
  <!-- Container -->
  <div class="relative h-[calc(100vh-64px)] w-full overflow-hidden">
    <!-- MOBILE: Fullscreen Poster with Gradient & Overlay -->
    <div class="absolute inset-0 lg:hidden">
      <img src={poster} alt={`Poster for ${title}`} class="h-full w-full object-cover" />
      <div class="from-background via-background/60 absolute inset-0 bg-gradient-to-t to-transparent"></div>
    </div>
  
    <!-- Content Wrapper -->
    <div class="relative z-10 flex h-full w-full flex-col justify-end lg:flex-row lg:justify-normal lg:p-12">
      <!-- DESKTOP Poster -->
      <div class="hidden w-2/5 items-center justify-center lg:flex">
        <img
          src={poster}
          alt={`Poster for ${title}`}
          class="max-h-[90%] rounded-xl object-cover shadow-lg"
        />
      </div>
  
      <!-- Info Panel -->
      <div class="mt-auto flex w-full flex-col justify-between p-6 lg:mt-0 lg:w-3/5 lg:bg-transparent lg:px-10 lg:py-6">
        <!-- Top Content -->
        <div class="lg:mb-auto">
          <h1 class="text-4xl font-bold drop-shadow">
            {title}
            <span class="text-muted-foreground text-2xl font-normal">({year})</span>
          </h1>
  
          <!-- Description with 2-line clamp on mobile -->
          <p
            class="text-muted-foreground mt-4 text-base text-balance max-w-2xl cursor-pointer transition-all duration-300 lg:cursor-default"
            class:line-clamp-2={!showFullDescription}
            on:click={toggleDescription}
          >
            {description}
          </p>
  
          <div class="mt-4 flex flex-wrap gap-2">
            {#each genres as genre}
              <Badge>{genre}</Badge>
            {/each}
          </div>
  
          <div class="text-muted-foreground mt-6 hidden space-y-1 text-sm lg:block">
            <p><span class="font-semibold">Starring:</span> {actors.join(', ')}</p>
            <p><span class="font-semibold">Director:</span> {director}</p>
          </div>
        </div>
  
        <!-- Action Buttons -->
        <div class="mt-6 flex gap-4 lg:mt-0">
          <Button size="icon"><ThumbsUp class="h-5 w-5" /></Button>
          <Button size="icon"><ThumbsDown class="h-5 w-5" /></Button>
          <Button variant="outline" size="icon"><Bookmark class="h-5 w-5" /></Button>
          <Button variant="outline" size="icon"><X class="h-5 w-5" /></Button>
        </div>
      </div>
    </div>
  </div>
  
  <style>
    /* Only apply line clamp when showFullDescription is false */
    .line-clamp-2 {
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
  </style>
  