<template>
  <div class="grid">
    <div class="cell">
      <BrandChart @pick="pass" />
    </div>

    <div class="cell">
      <CategoryChart @pick="pass" />
    </div>

    <div class="cell">
      <ItemHotChart @pick="pass" />
    </div>

    <div class="cell">
      <UserChart @pick="pass" />
    </div>
  </div>
</template>

<script setup>
import BrandChart from "@/components/BrandChart.vue"
import CategoryChart from "@/components/CategoryChart.vue"
import ItemHotChart from "@/components/ItemHotChart.vue"
import UserChart from "@/components/UserChart.vue"

const emit = defineEmits(["pick"])

const pass = (name) => emit("pick", name)
</script>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  height: 100%;
}

.cell {
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 8px;
  padding: 8px;
  min-height: 300px;
}

@media (max-width: 1000px) {
  .grid {
    grid-template-columns: 1fr;
    height: auto;
  }
}
</style>
