<script lang="ts">
  export let src: string = null;
  export let size: string | number = 1;
  export let color: string = null;
  export let flipH = null;
  export let flipV = null;
  export let rotate = 0;
  export let spin: boolean | number = false;
  let clazz = "";
  export { clazz as class };
  let path: string = undefined;
  let use: string = undefined;
  let url: string = undefined;
  //Icon source
  $: if (!!src && src.toLowerCase().trim().endsWith(".svg")) {
    url = src;
    path = use = undefined;
  } else if (!!src && src.toLowerCase().trim().includes(".svg#")) {
    use = src;
    url = path = undefined;
  } else if (!!src) {
    path = src;
    url = use = undefined;
  }
  // SPIN properties
  $: inverse = typeof spin !== "boolean" && spin < 0 ? true : false;
  $: spintime = Math.abs(spin === true ? 2 : <number>spin);
  $: spinCW = !!spin && !inverse;
  $: spinCCW = !!spin && inverse;
  // size
  if (Number(size)) size = Number(size);

  // styles
  function getStyles(size: number | string, color: string, flipH: boolean, flipV: boolean, rotate: number): string {
    const transform = [];
    const styles = [];
    if (size !== null) {
      const width = typeof size === "string" ? size : `${size * 1.5}rem`;
      styles.push(["width", width]);
      styles.push(["height", width]);
    }
    styles.push(["fill", color !== null ? color : "currentColor"]);
    if (flipH) {
      transform.push("scaleX(-1)");
    }
    if (flipV) {
      transform.push("scaleY(-1)");
    }
    if (rotate != 0) {
      transform.push(`rotate(${rotate}deg)`);
    }
    if (transform.length > 0) {
      styles.push(["transform", transform.join(" ")]);
      styles.push(["transform-origin", "center"]);
    }
    return styles.reduce((cur, item) => {
      return `${cur} ${item[0]}:${item[1]};`;
    }, "");
  }
  $: style = getStyles(size, color, flipH, flipV, rotate);
  $: aniStyle = !!spin ? `animation-duration: ${spintime}s` : undefined;
</script>

{#if url}
  <span {style} class={clazz} {...$$restProps}>
    <img src={url} alt="" width="100%" height="100%" class:spinCW class:spinCCW style={aniStyle} />
  </span>
{:else if use}
  <svg viewBox="0 0 24 24" {style} class={clazz} {...$$restProps}>
    <use xlink:href={use} class:spinCW class:spinCCW style={aniStyle} />
  </svg>
{:else}
  <svg viewBox="0 0 24 24" {style} class={clazz} {...$$restProps}>
    {#if spin !== false}
      <g class:spinCW class:spinCCW style={aniStyle}>
        <path d={path} />
      </g>
    {:else}
      <path d={path} />
    {/if}
  </svg>
{/if}

<style>
  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
  @keyframes spin-inverse {
    to {
      transform: rotate(-360deg);
    }
  }
  svg {
    vertical-align: middle;
  }
  span {
    display: inline-block;
    line-height: 1;
  }
  span img {
    padding: 0px;
    margin: 0px;
    vertical-align: middle;
  }
  .spinCW {
    animation: spin linear 2s infinite;
    transform-origin: center;
  }
  .spinCCW {
    animation: spin-inverse linear 2s infinite;
    transform-origin: center;
  }
</style>
