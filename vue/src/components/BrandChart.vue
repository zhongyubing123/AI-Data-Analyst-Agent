<template>
  <div ref="chart" class="chart"></div>
</template>

<script setup>
import * as echarts from "echarts"
import { ref, onMounted, onBeforeUnmount } from "vue"
import axios from "axios"

const emit = defineEmits(["pick"])

const chart = ref(null)
let myChart = null
let observer = null

const TOP = 10

const toWan = (value) => (Number(value) / 10000).toFixed(1)

onMounted(async () => {
  try {
    const { data } = await axios.get("/api/brand/sales")

    const list = data.slice(0, TOP).map(item => ({
      name: item.brand,
      value: Number(item.salesAmount) || 0
    }))

    const rest = data.slice(TOP).reduce((sum, item) => sum + (Number(item.salesAmount) || 0), 0)

    if (rest > 0) {
      list.push({ name: "其他品牌", value: rest })
    }

    // 横向条形图从上到下按金额递减
    list.reverse()

    myChart = echarts.init(chart.value)

    myChart.setOption({
      title: { text: "品牌销售额 Top10（万元）", left: 8, top: 6, textStyle: { fontSize: 13 } },
      grid: { left: 90, right: 60, top: 40, bottom: 20 },
      tooltip: {
        trigger: "axis",
        axisPointer: { type: "shadow" },
        formatter: (params) => {
          const p = params[0]
          return `${p.name}<br/>销售额：${toWan(p.value)} 万元`
        }
      },
      xAxis: { type: "value", splitLine: { show: false }, axisLabel: { show: false } },
      yAxis: {
        type: "category",
        data: list.map(item => item.name),
        axisTick: { show: false },
        axisLine: { show: false }
      },
      series: [
        {
          type: "bar",
          data: list.map(item => item.value),
          barMaxWidth: 18,
          itemStyle: { borderRadius: [0, 4, 4, 0] },
          label: {
            show: true,
            position: "right",
            formatter: (p) => toWan(p.value),
            fontSize: 11
          }
        }
      ]
    })

    myChart.on("click", (params) => {
      if (params.name !== "其他品牌") emit("pick", params.name)
    })

    observer = new ResizeObserver(() => myChart?.resize())
    observer.observe(chart.value)
  } catch (e) {
    console.error("加载品牌销售数据失败", e)
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
