<script context="module">
	export const ssr = false;

</script>

<script lang="ts">
	import Button from '../../components/basic/Button.svelte';
	import MuiIcon from '../..//components/MUIIcon.svelte';
	import { onMount } from 'svelte';
	import { fetch_api, getBaseUrl, fetch_file, put_file } from '$lib/servercalls';
	import MonacoEditor from '../../components/MonacoEditor.svelte';

	import ModalOverlay from '../../components/basic/ModalOverlay.svelte';

	let dlgVisible = false;


	let directory = [];
	let currentFile = '';
	let currentFilename = '';
	let currentValue = currentFile;
	let dirty = false;
	$: dirty = currentValue !== currentFile;

	function loadDirs(){
		fetch_api('api/fs/dir/scenes/').then((data: any) => {
			directory = data;
		});
	}
	onMount(() => {
		loadDirs();
	});

	function load(filename) {
		currentFilename = filename;
		fetch_file(filename).then((src) => {
			console.log('DONE');
			console.log(src);
			currentFile = src;
		});
	}

	function save(filename, val) {
		currentFilename = filename;
		put_file(filename, val).then(()=>loadDirs())
	}

	let newFilename=""
	function createNew(){
		if (!newFilename.endsWith('.py')) newFilename=newFilename+".py"
		currentFilename="/scenes/"+newFilename
		newFilename=""
		currentFile=""
		dlgVisible=false
	}
</script>

<div class="p-4 grid grid-cols-1 lg:grid-cols-5 bg-theme-background h-full gap-4 auto-rows-fr	">
	<div class="bg-theme-surface shadow-md rounded-lg">
		<div class="w-full pt-1 px-2 bg-theme-primary rounded-t-lg text-theme-onPrimary">Lichtband</div>
		<div class="flex flex-col p-2 gap-y-1">
			<div class="justify-self-end bg-theme-primary self-end px-4 py-2 rounded-md text-theme-onPrimary cursor-pointer"
			on:click={()=>dlgVisible=true}>create new</div>
			{#each directory as dir}
				<div class="flex flex-row">
					<button class="place-self-center" on:click={() => load(dir.name)}
						><MuiIcon icon="edit" size="sm" class="align-middle " /></button
					>
					<span class="flex-grow">{dir.name}</span>
				</div>
			{/each}
		</div>
	</div>
	<div class="bg-theme-surface shadow-md rounded-lg lg:col-span-4 flex flex-col">
		<div class="w-full pt-1 px-2 bg-theme-primary rounded-t-lg text-theme-onPrimary">
			Lichtband ({currentFilename})
		</div>
		<MonacoEditor src={currentFile} bind:currentValue class="flex-grow" />
		<!-- <textarea class="flex-grow overflow-scroll pl-4 py-2 font-mono" bind:value={currentFile} wrap="soft"/> -->
		<!-- <div class="flex-grow overflow-scroll border-l-8 border-theme-primaryLight pl-3">
                <pre contenteditable="true" bind:textContent={currentFile} class=" font-mono"></pre>
            </div> -->
		<div class="bg-theme-surface rounded-b-lg p-2 flex flex-row justify-items-end gap-x-4">
			<span class="flex-grow" />
			<button
				class="py-2 px-3 bg-theme-primary disabled:bg-theme-primaryLight text-theme-onPrimary rounded-md"
				disabled={!dirty}
				on:click={() => save(currentFilename, currentValue)}>Save</button
			>
		</div>
	</div>
</div>


<!-- New Scene Dialog -->
<ModalOverlay bind:visible={dlgVisible}>
	<div class="h-full w-full grid grid-cols-1 justify-items-center items-center grid-rows-1">
		<div class="bg-theme-primary rounded-md shadow-md w-60" on:click|stopPropagation={() => {}}>
			<div class="py-2 px-4 text-theme-onPrimary">HEADER</div>
			<div class=" bg-theme-surface text-theme-onSurface p-4 grid grid-cols-2 auto-rows-min">
				<span class="col-span-2 mb-4">Create new Scene, please enter Name:</span>
				<div>Scene Name:</div>
				<input type="text" class="border px-1" bind:value={newFilename}/>
			</div>
			<div class="bg-theme-surface py-5 flex flex-row justify-center rounded-b-md">
				<button class="py-2- px-4 bg-theme-primary rounded-md text-theme-onPrimary self-center"
				on:click={()=>createNew()}>
					create
				</button>
			</div>
		</div>
	</div>
</ModalOverlay>
