<script lang="ts">
	import { text } from 'svelte/internal';
	import ModalOverlay from '../../components/basic/ModalOverlay.svelte';
	let visible = false;
</script>

<button class="p-2 bg-theme-primary" on:click={() => (visible = !visible)}>Show</button>

<ModalOverlay bind:visible>
	<div class="h-full w-full grid grid-cols-1 justify-items-center items-center grid-rows-1">
		<div class="bg-theme-primary rounded-md shadow-md w-60" on:click|stopPropagation={() => {}}>
			<div class="py-2 px-4 text-theme-onPrimary">HEADER</div>
			<div class=" bg-theme-surface text-theme-onSurface p-4 grid grid-cols-2 auto-rows-min">
				<span class="col-span-2 mb-4">Create new Scene, please enter Name:</span>
				<div>Scene Name:</div>
				<input type="text" class="border px-1" value=""/>
			</div>
			<div class="bg-theme-surface py-5 flex flex-row justify-center rounded-b-md">
				<button class="py-2- px-4 bg-theme-primary rounded-md text-theme-onPrimary self-center">
					create
				</button>
			</div>
		</div>
	</div>
</ModalOverlay>
