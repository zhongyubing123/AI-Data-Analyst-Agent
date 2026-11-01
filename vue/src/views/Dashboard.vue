<template>
  <div class="grid">
    <div class="cell">
      <BrandChart />
    </div>

    <div class="cell">
      <CategoryChart />
    </div>

    <div class="cell">
      <ItemHotChart />
    </div>

    <div class="cell">
      <DailyTrendChart />
    </div>
  </div>
</template>

<script setup>
import BrandChart from "@/components/BrandChart.vue"
import CategoryChart from "@/components/CategoryChart.vue"
import ItemHotChart from "@/components/ItemHotChart.vue"
import DailyTrendChart from "@/components/DailyTrendChart.vue"
</script>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.cell {
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 8px;
  padding: 8px;
  height: 320px;
}

@media (max-width: 900px) {
  .grid {
    grid-template-columns: 1fr;
  }
}
</style>
