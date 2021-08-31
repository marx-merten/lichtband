<script lang="ts">
  import { fade, fly } from "svelte/transition";
  export let left = "0px";
  export let right = "0px";
  export let top = "0px";
  export let bottom = "0px";
  export let absolute = false;

  export let visible = false;
</script>

{#if visible}
<div
  class="{absolute ? 'absolute' : 'fixed'}  bg-theme-background bg-opacity-75 z-modal "
  style="top:{top};left:{left};right:{right};bottom:{bottom}"
  transition:fade
  on:click={() => (visible = false)}

>
  <slot />
</div>
{/if}