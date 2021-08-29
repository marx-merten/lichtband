
<script lang="ts">
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();
    export let checked=false
    let checkedClazz=""
    $:{
      checkedClazz=checked?"bg-theme-secondary":"bg-theme-primary"
    }
  </script>

<button type="button" class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md shadow-sm  hover:bg-theme-secondary    text-theme-onPrimary {checkedClazz} "
on:click={(ev) => dispatch("click", ev.detail)}>
    <slot/>
</button>
