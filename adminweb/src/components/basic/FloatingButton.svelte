<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { media } from "../../state/global-state";

  const dispatch = createEventDispatcher();
  import Icon from "../MUIIcon.svelte";
  export let icon: string;
</script>

<div class="fixed z-front right-2   " class:bottom-24={!$media.lg} class:bottom-10={$media.lg}>
  <button
    class="w-14 h-14 p-4  rounded-full elevation-10 bg-theme-secondary text-theme-onSecondary"
    on:click={(ev) => dispatch("click", ev.detail)}
  >
    <Icon {icon} size="md" /></button
  >
</div>
