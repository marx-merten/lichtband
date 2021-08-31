<script lang="ts">
	import { onMount } from 'svelte';
    import '../lib/monaco.d.ts'
	export let src = '';
    export let currentValue = src;
	let clazz = '';
	export { clazz as class };

	// @ts-ignore

	require.config({ paths: { vs: 'https://unpkg.com/monaco-editor@latest/min/vs' } });

	let container;
	let _editor: monaco.editor.IStandaloneCodeEditor;
	// @ts-ignore
	onMount(() => {
		require(['vs/editor/editor.main'], // @ts-ignore
        function () {
			// @ts-ignore
			_editor = monaco.editor.create(container, {
				value: src,
				language: 'python'
			});
            _editor.getModel().onDidChangeContent((ev)=>{
                console.log(_editor.getValue())
                currentValue=_editor.getValue()

            })
		});
	});

	function loadSrc(srcTxt) {
 		if (_editor !== undefined)
            _editor.setValue(srcTxt);
	}

	$: loadSrc(src)
</script>

<div bind:this={container} class={clazz} />
