<script lang="ts">
  export let icon: string;
  let clazz: string = "";
  export let size: "sm" | "md" | "lg" | "xl" = "md";

  export { clazz as class };
  let sizeClazz = "md-24";
  $: {
    sizeClazz = { sm: "md-18", md: "md-24", lg: "md-36", xl: "md-48" }[size];
  }
</script>

<div class="material-icons {sizeClazz} {clazz}">{icon}</div>
