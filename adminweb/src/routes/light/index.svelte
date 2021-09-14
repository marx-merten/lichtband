<script lang="ts">
	import { onMount } from 'svelte';
	import Button from '../../components/basic/Button.svelte';
	import Icon from '../../components/MUIIcon.svelte';
	import { fetch_api } from '$lib/servercalls';
	import { fetch_light_state, lightState } from '$lib/backend';

    import { ColorPicker, Color } from 'svelte-colorpick'
    let color = Color.rgb({'r':200,'g':100,'b':90})

    function setColor(col){
        color=col
    }
    $:{

        setColor(Color.rgb({'r':$lightState.rgb.red,'g':$lightState.rgb.green,'b':$lightState.rgb.blue}))
    }

    const showSliders = {'hsl.h':true}
	// TODO Add overlay while switching
	function update() {
		fetch_light_state();
	}

	function toggle() {
		const newState = $lightState.state ? 'False' : 'True';
		fetch_api('api/light/switch?state=' + newState).then(() => {
			update();
		});
	}
	function activateScene(scene: string) {
		fetch_api('api/light/switch?scene=' + scene).then(() => {
			update();
		});
	}

	onMount(() => {
		update();
	});
</script>

<div
	class="p-5 h-full w-full bg-theme-background grid grid-cols-1 lg:grid-cols-2 gap-4 auto-rows-max "
>
	<div class="bg-theme-surface shadow-md rounded-lg pb-4">
		<div class="w-full pt-1 px-2 bg-theme-primary rounded-t-lg text-theme-onPrimary grid grid-rows-1 grid-flow-col flex-shrink-0 ">
            <span>Status</span>
            <span class="justify-self-end cursor-pointer" on:click={update} >
                <Icon icon="refresh" />
            </span>
        </div>
		<div class="grid grid-cols-1 auto-rows-auto">
			<div class="justify-self-center">
				<button on:click={toggle}
					><Icon
						icon="lightbulb"
						size="xxl"
						class={$lightState.state ? 'text-orange-500' : 'text-grey-700'}
					/>
				</button>
			</div>
			{#if $lightState.state}
				<div
					class="h-9 w-9 border-theme-primary border justify-self-center"
					style="background:rgb({$lightState.rgb.red},{$lightState.rgb.green},{$lightState.rgb.blue})"
				/>
                <!-- <ColorPicker bind:color={color} {showSliders}/> -->

                <!-- <p>Your color is currently {color.toHex()}</p> -->
			{/if}
			{#if $lightState.sceneActive}
				<div class="justify-self-center text-2xl">
					{$lightState.currentScene}
				</div>
			{/if}
		</div>
	</div>
	<div class="bg-theme-surface shadow-md rounded-lg">
		<div class="w-full pt-1 px-2 bg-theme-primary rounded-t-lg text-theme-onPrimary">Szenen</div>
		<div class="grid grid-cols-1 auto-rows-auto py-2 px-2 gap-2">
			{#each $lightState.scenes as sc}
				<div class="grid grid-rows-1">
					<Button
						checked={sc == $lightState.currentScene}
						on:click={() => {
							activateScene(sc);
						}}>{sc}</Button
					>
				</div>
			{/each}
		</div>
	</div>
</div>
