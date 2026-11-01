<template>
  <div ref="chart" class="chart"></div>
</template>

<script setup>
import * as echarts from "echarts"
import { ref, onMounted, onBeforeUnmount } from "vue"
import axios from "axios"

const chart = ref(null)
let myChart = null
let observer = null

const toWan = (value) => (Number(value) / 10000).toFixed(1)

onMounted(async () => {
  try {
    const { data } = await axios.get("/api/daily/trend")

    myChart = echarts.init(chart.value)

    myChart.setOption({
      title: { text: "每日成交额（万元）", left: 8, top: 6, textStyle: { fontSize: 13 } },
      grid: { left: 60, right: 24, top: 50, bottom: 40 },
      tooltip: {
        trigger: "axis",
        formatter: (params) => {
          const p = params[0]
          return `${p.name}<br/>成交额：${toWan(p.value)} 万元`
        }
      },
      xAxis: {
        type: "category",
        data: data.map(item => item.dt),
        axisTick: { show: false },
        axisLine: { lineStyle: { color: "rgba(255,255,255,.25)" } },
        axisLabel: { fontSize: 11 }
      },
      yAxis: {
        type: "value",
        splitLine: { lineStyle: { color: "rgba(255,255,255,.08)" } },
        axisLabel: { formatter: (v) => (v / 10000).toFixed(0) }
      },
      series: [
        {
          type: "line",
          smooth: true,
          symbolSize: 6,
          data: data.map(item => Number(item.salesAmount) || 0),
          areaStyle: { opacity: 0.15 },
          lineStyle: { width: 2 }
        }
      ]
    })

    observer = new ResizeObserver(() => myChart?.resize())
    observer.observe(chart.value)
  } catch (e) {
    console.error("加载每日趋势失败", e)
  }
})

onBeforeUnmount(() => {
  observer?.disconnect()
  myChart?.dispose()
})
</script>

<style scoped>
.chart {
  width: 100%;
  height: 100%;
  min-height: 260px;
}
</style>
