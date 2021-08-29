

<script lang="ts">
    import { onMount } from 'svelte';
	import Button from '../../components/basic/Button.svelte';
	import Icon from '../../components/MUIIcon.svelte';
	import { fetch_api } from '$lib/servercalls';

	let status = {
		sceneState: false,
		state: false,
		scenes: [],
		rgbw: [0, 0, 0, 255],
		activeScene: 'None'
	};


	function update() {
		fetch_api('light/status').then((state: any) => {
			status = state;
		});
	}

    function toggle(){
        const newState=status.state?"False":"True"
        fetch_api('light/switch?state='+newState).then( ()=>{
            update()
        })
    }
    function activateScene(scene:string){
        fetch_api('light/switch?scene='+scene).then( ()=>{
            update()
        })
    }


    onMount(()=>{update()})

</script>

<div
	class="p-5 h-full w-full bg-theme-background grid grid-cols-1 lg:grid-cols-2 gap-4 auto-rows-max "
>
	<div class="bg-theme-surface shadow-md rounded-lg">
		<div class="w-full pt-1 px-2 bg-theme-primary rounded-t-lg text-theme-onPrimary">Lichtband</div>
		<div class="grid grid-cols-1 auto-rows-auto">
			<div class="justify-self-center">
				<button on:click={toggle}><Icon
					icon="lightbulb"
					size="xxl"
					class={status.state ? 'text-orange-500' : 'text-grey-700'}
				/>
            </button>
			</div>
            {#if status.sceneState}
            <div class="justify-self-center text-2xl">
                {status.activeScene}
			</div>
            {/if}
		</div>
	</div>
	<div class="bg-theme-surface shadow-md rounded-lg">
		<div class="w-full pt-1 px-2 bg-theme-primary rounded-t-lg text-theme-onPrimary">Szenen</div>
		<div class="grid grid-cols-1 auto-rows-auto py-2 px-2 gap-2">
            {#each status.scenes as sc}
                <div class="grid grid-rows-1">
                    <Button checked={sc==status.activeScene}  on:click={()=>{activateScene(sc)}}>{sc}</Button>
                </div>
            {/each}

        </div>
    </div>
    <div class="p-3 border-2 border-red-200  col-span-full">
		<Button on:click={update}><Icon icon="refresh" size="md" /></Button>
	</div>
</div>
