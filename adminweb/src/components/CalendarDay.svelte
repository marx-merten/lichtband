<script lang="ts">
  export let currentDate = new Date();
  export let size: "sm" | "lg" = "lg";
  import { dateformat } from "../../lib/format";
</script>

{#if size == "lg"}
  <div class=" bg-theme-surface h-42 p-3 mt-2 font-medium ">
    <div class="w-20 flex-none  text-center rounded-lg elevation-4">
      <div class="bg-theme-secondaryLight rounded-t-lg text-theme-onSecondary py-1">
        {dateformat(currentDate, "mmmm")}
      </div>
      <div class="pt-1   bg-theme-surface">
        <span class="text-2xl font-bold leading-tight"> {dateformat(currentDate, "dd")} </span>
      </div>
      <div class="rounded-b-lg text-center  bg-theme-surface -pt-2 mb-1">
        <span class="text-sm"> {dateformat(currentDate, "dddd")} </span>
      </div>
    </div>
  </div>
{:else}
  <div class=" bg-theme-surface  font-medium ">
    <div class="w-12 flex-none  text-center rounded-lg elevation-4">
      <div class="bg-theme-secondaryLight rounded-t-lg text-theme-onSecondary py-1 h-4" />
      <div class="  bg-theme-surface -mb-1">
        <span class="text-sm font-extrabold leading-tight"> {dateformat(currentDate, "dd")} </span>
      </div>
      <div class="rounded-b-lg text-center  bg-theme-surface -pt-2 mb-1">
        <span class="text-sm"> {dateformat(currentDate, "ddd")} </span>
      </div>
    </div>
  </div>
{/if}
