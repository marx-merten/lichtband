<script lang="ts">
	import ModalOverlay from '../../components/basic/ModalOverlay.svelte';

	import { fetch_api, put_file } from '$lib/servercalls';

	import CryptoJS from 'crypto-js/core.js';
	import SHA256 from 'crypto-js/sha256.js';
	let dlgVisible = false;
	let dlgCallback: () => void;
	let dlgTitle: string;
	let dlgButton: string;
	let dlgSummary: string;

	let firmwareFiles: FileList;
	let firmwareFile: File;
	let firmwareSHA: string;
	let deviceSHA: string;

	$: {
		if (firmwareFiles !== undefined && firmwareFiles.length > 0) {
			firmwareFile = firmwareFiles[0];

			let fileReader = new FileReader();
			fileReader.onload = function (evt) {
				if (evt.target.readyState == FileReader.DONE) {
					var arrayBuffer = evt.target.result;

					firmwareSHA= SHA256(CryptoJS.enc.Latin1.parse(evt.target.result));

				}
			};
			fileReader.readAsBinaryString(firmwareFile);
		}
	}
	function showDlg(title: string, txt: string, button = 'OK', cb = () => {}) {
		if (!dlgVisible) {
			dlgTitle = title;
			dlgSummary = txt;
			dlgCallback = cb;
			dlgButton = button;
			dlgVisible = true;
		}
	}
	function hideDlg() {
		dlgVisible = false;
	}
	function resetIOT(event: MouseEvent) {
		showDlg('Reset Device', 'Are you sure you want to reset the Device.', 'Reset', async () => {
			await fetch_api('api/kernel/sys/reset');
			hideDlg();
		});
	}

	function activateFirmware(event: MouseEvent) {
		showDlg('Update Device', 'Are you sure you want to update and reset the Device.', 'Reset', async () => {
			await fetch_api('api/kernel/ota/activate', { headers: { 'X-OTA-CHECKSUM': deviceSHA } });
			hideDlg();
		});
	}
	function uploadFirmware(event: MouseEvent) {
		deviceSHA = 'UPLOADING';
		fetch_api('api/kernel/ota/upload', { method: 'PUT', body: firmwareFile }).then((response) => {
			deviceSHA = response.sha256;
		});
	}
</script>

<div class="p-5 lg:p-8">
	<div class="bg-white overflow-hidden shadow rounded-lg divide-y divide-gray-200">
		<div class="px-4 py-3 sm:px-6 text-theme-onPrimary bg-theme-primary font-medium">System Commands</div>
		<div class="px-4 py-5 sm:p-6 grid grid-cols-2 lg:grid-cols-3 auto-rows-min">
			<button class="bg-theme-primary rounded-md text-theme-onPrimary py-2 px-4" on:click={resetIOT}>
				Reset LEDs
			</button>
		</div>
	</div>

	<div class="bg-white overflow-hidden shadow rounded-lg divide-y divide-gray-200 mt-4">
		<div class="px-4 py-3 sm:px-6 text-theme-onPrimary bg-theme-primary font-medium">Update Firmware</div>
		<div class="px-4 py-5 sm:p-6 grid grid-cols-1 lg:grid-cols-3 auto-rows-min">
			<div class=" flex flex-col">
				<input type="file" bind:files={firmwareFiles} />
			</div>
			<div class="lg:col-span-2">
				{#if firmwareFile !== undefined}
					<div class="mt-2">
						<p>Firmware Selected : {firmwareFile?.name}</p>
						<p>Firmware SHA256 : {firmwareSHA}</p>
						<button class="bg-theme-primary rounded-md text-theme-onPrimary py-2 px-4" on:click={uploadFirmware}>
							Upload
						</button>
						{#if deviceSHA !== undefined}
							<p>Device SHA: {deviceSHA}</p>
							{#if deviceSHA !== 'UPLOADING'}
								<button class="bg-theme-primary rounded-md text-theme-onPrimary py-2 px-4" on:click={activateFirmware}>
									activate & Reset
								</button>
							{/if}
						{/if}
					</div>
				{/if}
			</div>
		</div>
	</div>
</div>

<!-- New Scene Dialog -->
<ModalOverlay bind:visible={dlgVisible}>
	<div class="h-full w-full grid grid-cols-1 justify-items-center items-center grid-rows-1">
		<div class="bg-theme-surface text-theme-onSurface shadow sm:rounded-lg" on:click|stopPropagation={() => {}}>
			<div class="px-4 py-5 sm:p-6">
				<h3 class="text-lg leading-6 font-medium ">{dlgTitle}</h3>
				<div class="mt-2 max-w-xl text-sm ">
					<p>{dlgSummary}</p>
				</div>
				<div class="mt-5">
					<button
						type="button"
						class="inline-flex items-center justify-center px-4 py-2 border border-transparent font-medium rounded-md text-theme-onPrimary bg-theme-primary hover:bg-theme-secondary focus:outline-none focus:ring-2 focus:ring-offset-2  sm:text-sm"
						on:click={() => {
							dlgCallback();
						}}
					>
						{dlgButton}
					</button>
				</div>
			</div>
		</div>
	</div>
</ModalOverlay>
