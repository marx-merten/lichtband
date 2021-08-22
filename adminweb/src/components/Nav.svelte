<script lang="ts">
  import type { NavRoute } from "../lib/Interface";
  import ModalOverlay from "./basic/ModalOverlay.svelte";
  import Icon from "./MUIIcon.svelte";
  let clazz = "";
  export { clazz as class };

  export let segment: string;
  export let routes: NavRoute[] = [];
  export let vertical = false;
  export let collapsed = false;
  export let maxItems = 5;
  let maxItemsDisplay = 5;
  $: {
    maxItemsDisplay = routes.length > maxItems ? maxItems - 1 : maxItems;
  }
  let showDlg = false;
  const cssItem = "overflow-hidden overflow-ellipsis w-14 h-12 justify-end text-theme-onPrimaryInactive";
  const cssItemSelected = "overflow-hidden overflow-ellipsis w-14 text-theme-secondary   h-12 justify-end";
  $: console.log("NAV", vertical);
</script>

{#if vertical}
  <nav class="flex flex-col h-full w-full justify-start items-end {clazz}">
    <div class="h-32 flex flex-col pr-4 pt-8 ">
      <Icon icon="dvr" size="xl" class="self-end " />
      <div class="transform origin-top-left -rotate-90 translate-x-3 translate-y-4 italic font-bold">EPG@Home</div>
    </div>
    {#each routes as route}
      <a href={route.path}>
        <div class="w-full flex flex-row {segment == route.segment ? cssItemSelected : cssItem} mt-4">
          <div class="text-lg   pl-2 self-center" class:hidden={collapsed}>{route.label}</div>
          <Icon icon={route.icon} size="xl" class="px-4" />
        </div>
      </a>
    {/each}
    <div class="h-full flex-grow" />
    <div class="mr-2 mb-2" on:click={() => (collapsed = !collapsed)}>
      <Icon icon="navigate_{collapsed ? 'next' : 'before'}" class="text-theme-onPrimaryInactive " size="xl" />
    </div>
  </nav>
{:else}
  <nav class="flex h-full">
    <div class="flex-1 flex flex-row justify-evenly self-center  ">
      {#each routes as route, idx}
        {#if idx < maxItemsDisplay}
          <a href={route.path} on:click={() => (showDlg = false)}>
            <div class="flex flex-col {segment == route.segment ? cssItemSelected : cssItem}">
              <div class="material-icons md-24 self-center">{route.icon}</div>
              <div class="text-sm  self-center">{route.label}</div>
            </div>
          </a>
        {/if}
      {/each}
      {#if routes.length > maxItems}
        <div class="flex flex-col {cssItem}">
          <div
            class="material-icons md-24 self-center"
            on:click={() => {
              showDlg = !showDlg;
            }}
          >
            more_vert
          </div>
          <div class="text-sm  self-center">&nbsp</div>
        </div>
      {/if}
    </div>
  </nav>
{/if}
<ModalOverlay bind:visible={showDlg} bottom="75px">
  <div class="h-full w-full relative flex flex-col justify-end">
    <div class="w-full bg-theme-surface flex flex-col pr-8">
      {#each routes as route, idx}
        {#if idx >= maxItemsDisplay}
          <a href={route.path}>
            <div class="w-full flex flex-row {segment == route.segment ? cssItemSelected : cssItem} mt-4">
              <div class="text-lg   pl-2 self-center">{route.label}</div>
              <Icon icon={route.icon} size="lg" class="px-4" />
            </div>
          </a>
        {/if}
      {/each}
    </div>
  </div></ModalOverlay
>
