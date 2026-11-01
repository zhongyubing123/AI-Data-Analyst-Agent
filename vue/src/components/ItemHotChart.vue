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

const shortName = (name) => (name && name.length > 12 ? name.slice(0, 12) + "…" : name)

onMounted(async () => {
  try {
    const { data } = await axios.get("/api/item/hot")

    const list = data.slice(0, TOP).map(item => ({
      name: item.itemName,
      value: Number(item.buyCount) || 0
    }))

    list.reverse()

    myChart = echarts.init(chart.value)

    myChart.setOption({
      title: { text: "商品销量 Top10（次）", left: 8, top: 6, textStyle: { fontSize: 13 } },
      grid: { left: 150, right: 50, top: 40, bottom: 20 },
      tooltip: {
        trigger: "axis",
        axisPointer: { type: "shadow" },
        formatter: (params) => {
          const p = params[0]
          return `${p.name}<br/>销量：${p.value} 次`
        }
      },
      xAxis: { type: "value", splitLine: { show: false }, axisLabel: { show: false } },
      yAxis: {
        type: "category",
        data: list.map(item => shortName(item.name)),
        axisTick: { show: false },
        axisLine: { show: false },
        axisLabel: { fontSize: 11 }
      },
      series: [
        {
          type: "bar",
          data: list.map(item => item.value),
          barMaxWidth: 18,
          itemStyle: { borderRadius: [0, 4, 4, 0] },
          label: { show: true, position: "right", fontSize: 11 }
        }
      ]
    })

    myChart.on("click", (params) => {
      const index = params.dataIndex
      emit("pick", list[index]?.name || params.name)
    })

    observer = new ResizeObserver(() => myChart?.resize())
    observer.observe(chart.value)
  } catch (e) {
    console.error("加载商品销量数据失败", e)
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
