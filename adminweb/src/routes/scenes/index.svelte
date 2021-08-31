<script lang="ts">
	import Button from '../../components/basic/Button.svelte';
    import MuiIcon from '../..//components/MUIIcon.svelte';
    import { onMount } from 'svelte';
    import {fetch_api,getBaseUrl,fetch_file} from '$lib/servercalls'
    let directory = []
    let currentFile=""
    let currentFilename=""
    onMount(()=>{
        fetch_api("api/fs/dir/scenes/").then((data:any)=>{
            directory=data
        })
    })

    function load(filename){
        currentFilename=filename
        fetch_file(filename).then((src)=>{
            console.log("DONE")
            console.log(src)
            currentFile=src
        })
    }

</script>

<div class="p-4 grid grid-cols-1 lg:grid-cols-5 bg-theme-background h-full gap-4 auto-rows-fr	">
	<div class="bg-theme-surface shadow-md rounded-lg">
		<div class="w-full pt-1 px-2 bg-theme-primary rounded-t-lg text-theme-onPrimary">Lichtband</div>
		<div class="flex flex-col p-2 gap-y-1">
            {#each directory as dir}
                <div class="flex flex-row">
                    <button class="place-self-center" on:click={()=>load(dir.name)}><MuiIcon icon="edit" size="sm" class="align-middle " ></MuiIcon></button>
                    <span class="flex-grow">{dir.name}</span>
                </div>

            {/each}
        </div>
	</div>
	<div class="bg-theme-surface shadow-md rounded-lg lg:col-span-4 flex flex-col">
		<div class="w-full pt-1 px-2 bg-theme-primary rounded-t-lg text-theme-onPrimary">Lichtband ({currentFilename})</div>
			<textarea class="flex-grow overflow-scroll pl-4 py-2 font-mono" bind:value={currentFile} wrap="soft"/>
            <!-- <div class="flex-grow overflow-scroll border-l-8 border-theme-primaryLight pl-3">
                <pre contenteditable="true" bind:textContent={currentFile} class=" font-mono"></pre>
            </div> -->
                <div class="bg-theme-surface rounded-b-lg p-2 flex flex-row justify-items-end gap-x-4">
				<span class="flex-grow"/>
                <button class="py-2 px-3 bg-theme-primary text-theme-onPrimary rounded-md">Save</button>
			</div>

	</div>
</div>
