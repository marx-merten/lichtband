<script lang="ts">
	import MuiIcon from '../../components/MUIIcon.svelte';
	import { fade } from 'svelte/transition';

	import { fetch_cfg, iotConfig, iotConfigChanged ,store_cfg} from '$lib/configStore';
	import { onMount } from 'svelte';
import { fetch_api } from '$lib/servercalls';
</script>

<div
	class="bg-theme-background
             py-4 px-2 lg:px-9
            h-full flex flex-col grid grid-cols-1  auto-rows-min lg:grid-cols-2   lg:gap-4">
		<div class="col-span-full font-bold text-2xl">Network:</div>

		<div>
			<label for="wlanSSID" class="block text-sm lg:text-lg font-medium text-gray-700"> WIFI Network </label>
			<div class="mt-1">
				<input
					type="text"
					name="wlanSSID"
					id="wlanSSID"
					class="shadow-sm focus:ring-theme-secondary focus:border-theme-secondary block w-full sm:text-sm border-gray-300 rounded-md"
					placeholder="<your SSID>"
					bind:value={$iotConfig.network.ssid}
				/>
				<!-- TODO Add Selector -->
			</div>
		</div>

		<div>
			<label for="wlanPass" class="block text-sm lg:text-lg font-medium text-gray-700"> WIFI Password </label>
			<div class="mt-1">
				<input
					type="password"
					name="wlanPass"
					id="wlanPass"
					class="shadow-sm focus:ring-theme-secondary focus:border-theme-secondary block w-full sm:text-sm border-gray-300 rounded-md"
					placeholder="<your WPA2>"
					bind:value={$iotConfig.network.password}
				/>
			</div>
		</div>

		<div class="col-span-full font-bold text-2xl">MQTT:</div>

		<div>
			<label for="mqttServer" class="block text-sm lg:text-lg font-medium text-gray-700"> Server </label>
			<div class="mt-1">
				<input
					type="text"
					name="mqttServer"
					id="mqttServer"
					class="shadow-sm focus:ring-theme-secondary focus:border-theme-secondary block w-full sm:text-sm border-gray-300 rounded-md"
					placeholder="<MQTT Server>"
					bind:value={$iotConfig.mqtt.server}
				/>
			</div>
		</div>

		<div>
			<label for="mqttPort" class="block text-sm lg:text-lg font-medium text-gray-700"> Port </label>
			<div class="mt-1">
				<input
					type="text"
					name="mqttPort"
					id="mqttPort"
					class="shadow-sm focus:ring-theme-secondary focus:border-theme-secondary block w-full sm:text-sm border-gray-300 rounded-md"
					placeholder="<Port>"
					bind:value={$iotConfig.mqtt.port}
				/>
			</div>
		</div>

		<div>
			<label for="mqttName" class="block text-sm lg:text-lg font-medium text-gray-700"> Devicename </label>
			<div class="mt-1">
				<input
					type="text"
					name="mqttName"
					id="mqttName"
					class="shadow-sm focus:ring-theme-secondary focus:border-theme-secondary block w-full sm:text-sm border-gray-300 rounded-md"
					placeholder="<IOT Devicename>"
					bind:value={$iotConfig.mqtt.name}
				/>
			</div>
		</div>

		<div class="col-start-">
			<label for="mqttPrefix" class="block text-sm lg:text-lg font-medium text-gray-700"> Prefix </label>
			<div class="mt-1">
				<input
					type="text"
					name="mqttPrefix"
					id="mqttPrefix"
					class="shadow-sm focus:ring-theme-secondary focus:border-theme-secondary block w-full sm:text-sm border-gray-300 rounded-md"
					placeholder="< Prefix>"
					bind:value={$iotConfig.mqtt.prefix}
				/>
			</div>
		</div>

		<div class="">
			<label for="mqttTopic" class="block text-sm lg:text-lg font-medium text-gray-700"> Online Topic </label>
			<div class="mt-1">
				<input
					type="text"
					name="mqttTopic"
					id="mqttTopic"
					class="shadow-sm focus:ring-theme-secondary focus:border-theme-secondary block w-full sm:text-sm border-gray-300 rounded-md"
					placeholder="<HELO Topic>"
					bind:value={$iotConfig.mqtt.online}
				/>
			</div>
		</div>

		<div class="col-span-full font-bold text-2xl">Led:</div>

		<div class="">
			<label for="leds" class="block text-sm lg:text-lg font-medium text-gray-700"> LED Count </label>
			<div class="mt-1 flex flex-row gap-4">
				<input
					type="number"
					name="leds"
					id="leds"
					class="shadow-sm focus:ring-theme-secondary focus:border-theme-secondary block w-full sm:text-sm border-gray-300 rounded-md"
					placeholder="<LED Count>"
					bind:value={$iotConfig.led.count}
				/>
				<button class="bg-theme-primary px-2 rounded-md text-theme-onPrimary flex flex-row place-items-center">
					<MuiIcon icon="lightbulb" size="md" />
					<span class="pl-2" on:click={()=>fetch_api("api/light/tools/size?size="+$iotConfig.led.count)}>TEST</span>
					<!-- Add LED Test via backend call-->
				</button>
			</div>
		</div>
		<div class="h-4 col-span-full"/>

	{#if $iotConfigChanged}
		<div class="col-span-full flex flex-row gap-4 justify-end w-full pt-4 pb-4" transition:fade>
			<button class="bg-theme-primary px-4 py-2 rounded-md text-theme-onPrimary" on:click={()=> store_cfg($iotConfig)}> save config </button>
			<button class="bg-theme-primary px-4 py-2 rounded-md text-theme-onPrimary" on:click={() => fetch_cfg()	}>
				reload from device
			</button>
		</div>
	{/if}
</div>