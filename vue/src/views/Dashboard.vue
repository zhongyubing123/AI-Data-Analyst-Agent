<template>
  <div>
    <h2 style="color:white">电商可视化大屏</h2>
    <BrandChart />
    <UserChart />
    <CategoryChart />
    <ItemHotChart />
  </div>
</template>

<script setup>
import BrandChart from "@/components/BrandChart.vue"
import UserChart from "@/components/UserChart.vue"
import CategoryChart from "@/components/CategoryChart.vue"
import ItemHotChart from "@/components/ItemHotChart.vue"
</script>