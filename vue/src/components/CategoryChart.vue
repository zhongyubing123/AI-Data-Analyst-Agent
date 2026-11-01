<template>
  <div ref="chart" class="chart"></div>
</template>

<script setup>
import * as echarts from "echarts"
import { ref, onMounted } from "vue"
import axios from "axios"

const emit = defineEmits(["pick"])

const chart = ref(null)

onMounted(async () => {
  const res = await axios.get("/api/category/sales")

  const myChart = echarts.init(chart.value)

  myChart.setOption({
    title: {
      text: "品类销售占比"
    },
    tooltip: {
      trigger: "item"
    },
    legend: {
      bottom: 0
    },
    series: [
      {
        type: "pie",
        radius: "60%",
        data: res.data.map(item => ({
          name: item.category,
          value: item.salesAmount
        }))
      }
    ]
  })

  window.addEventListener("resize", () => {
    myChart.resize()
  })
})
</script>

<style scoped>
.chart {
  width: 100%;
  height: 100%;
  min-height: 260px;
}
</style>
