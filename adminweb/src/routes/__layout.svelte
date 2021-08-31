<script lang='ts'>
import "../app.postcss";
export let segment: string;

import Nav from "../components/Nav.svelte";
import { page } from '$app/stores';


import { onMount } from "svelte";
import anylogger from "anylogger";
import { media } from "../state/global-state";
import { NavRoute } from "../lib/Interface";
const LOG = anylogger("App-Layout");
onMount(() => LOG("Inner Mount"));

const routes = [
  new NavRoute("light", "light", "LED", "home"),
  new NavRoute("status", "status", "Status", "list"),
  new NavRoute("scenes", "scenes", "Szenen", "collections"),
  new NavRoute("tools", "tools", "Tools", "settings"),
  new NavRoute("cfg", "cfg", "config", "settings"),
];

$:{
    segment=$page.path.split('/').slice(-1)[0]
}

</script>


<div class=" h-full" class:grid-container={!$media.lg} class:grid-containerXL={$media.lg}>
    <div class="grdNav   bg-theme-primary text-theme-onPrimary elevation-5 ">
      <Nav {segment} {routes} vertical={$media.lg} maxItems={5} class="z-tools" />
    </div>
    <main class="grdMain bg-theme-background overflow-y-scroll">
      <slot/>
    </main>
  </div>



<style lang="postcss">
    .grid-container {
      display: grid;
      grid-template-columns: minmax(0, 1fr);
      grid-template-rows: minmax(0, 1fr) 75px;
      gap: 0px 0px;
      grid-template-areas:
        "grdMain"
        "grdNav";
    }

    .grid-containerXL {
      display: grid;
      grid-template-columns: minmax(0, auto) minmax(0, 1fr);
      grid-template-rows: minmax(0, 1fr);
      gap: 0px 0px;
      grid-template-areas: "grdNav grdMain";
    }

    .grdNav {
      grid-area: grdNav;
    }

    .grdMain {
      grid-area: grdMain;
    }
  </style>
