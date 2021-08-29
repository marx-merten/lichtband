<script lang="ts">
	import { fetch_api } from '$lib/servercalls';
	import MuiIcon from '../../components/MUIIcon.svelte';
	let status = '';
	let statusJson = {};
	import { onMount } from 'svelte';
	function update_stats() {
		fetch_api('kernel/stats').then((dat) => {
			statusJson = dat;
			status = JSON.stringify(dat, null, 4); // Indented 4 spaces
		});
	}
	onMount(() => {
		update_stats();
	});
</script>

<div class="h-full w-full p-4">
	<div class="bg-theme-surface shadow-md rounded-lg h-full flex flex-col  ">
		<div class="w-full pt-1 px-2 bg-theme-primary rounded-t-lg text-theme-onPrimary grid grid-rows-1 grid-flow-col flex-shrink-0 ">
            <span>Status</span>
            <span class="justify-self-end" on:click={update_stats}>
                <MuiIcon icon="refresh" />
            </span>
        </div>
		<pre class="overflow-scroll place-self-stretch flex-grow">{status}</pre>
	</div>
</div>
