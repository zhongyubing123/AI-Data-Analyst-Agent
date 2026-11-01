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
  const res = await axios.get("/api/item/hot")

  const myChart = echarts.init(chart.value)

  myChart.setOption({
    title: {
      text: "商品热度排行"
    },
    tooltip: {
      trigger: "axis"
    },
    legend: {
      data: ["购买次数", "浏览次数"]
    },
    xAxis: {
      type: "category",
      data: res.data.map(item => item.itemName)
    },
    yAxis: {
      type: "value"
    },
    series: [
      {
        name: "购买次数",
        type: "bar",
        data: res.data.map(item => item.buyCount)
      },
      {
        name: "浏览次数",
        type: "bar",
        data: res.data.map(item => item.pvCount)
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
