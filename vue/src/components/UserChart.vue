<template>
  <div ref="chart" style="width:100%;height:400px"></div>
</template>

<script setup>
import * as echarts from "echarts"
import { ref, onMounted } from "vue"
import axios from "axios"

const chart = ref(null)

onMounted(async () => {
  const res = await axios.get("/api/user/active")

  const myChart = echarts.init(chart.value)

  myChart.setOption({
    title: {
      text: "用户活跃排行"
    },
    tooltip: {
      trigger: "axis"
    },
    xAxis: {
      type: "category",
      data: res.data.map(item => item.userId)
    },
    yAxis: {
      type: "value"
    },
    series: [
      {
        name: "购买次数",
        type: "bar",
        data: res.data.map(item => item.buyCount)
      }
    ]
  })

  window.addEventListener("resize", () => {
    myChart.resize()
  })
})
</script>