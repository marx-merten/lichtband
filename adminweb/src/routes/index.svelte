<script lang="ts">
    import { goto } from '$app/navigation';

    import { onMount } from 'svelte';



onMount(async () => {
    // Before loading vs/editor/editor.main, define a global MonacoEnvironment that overwrites
	// the default worker url location (used when creating WebWorkers). The problem here is that
	// HTML5 does not allow cross-domain web workers, so we need to proxy the instantiation of
	// a web worker through a same-domain script
	// @ts-ignore
	window.MonacoEnvironment = {
		getWorkerUrl: function (workerId, label) {
			return `data:text/javascript;charset=utf-8,${encodeURIComponent(`
        self.MonacoEnvironment = {
          baseUrl: 'https://unpkg.com/monaco-editor@latest/min/'
        };
        importScripts('https://unpkg.com/monaco-editor@latest/min/vs/base/worker/workerMain.js');`)}`;
		}
	};

    goto("/light")
});
  </script>
