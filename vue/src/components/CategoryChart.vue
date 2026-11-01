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

const toWan = (value) => (Number(value) / 10000).toFixed(1)

onMounted(async () => {
  try {
    const { data } = await axios.get("/api/category/sales")

    myChart = echarts.init(chart.value)

    myChart.setOption({
      title: {
        text: "品类销售占比（万元）",
        left: 8,
        top: 6,
        textStyle: { fontSize: 13 }
      },
      tooltip: {
        trigger: "item",
        formatter: (p) => `${p.name}<br/>${toWan(p.value)} 万元（${p.percent}%）`
      },
      legend: {
        bottom: 0,
        itemWidth: 10,
        itemHeight: 10,
        textStyle: { fontSize: 11 }
      },
      series: [
        {
          type: "pie",
          radius: ["42%", "66%"],
          center: ["50%", "46%"],
          avoidLabelOverlap: true,
          label: { show: false },
          labelLine: { show: false },
          itemStyle: { borderColor: "#fff", borderWidth: 2 },
          data: data.map((item) => ({
            name: item.category,
            value: Number(item.salesAmount) || 0
          }))
        }
      ]
    })

    myChart.on("click", (params) => emit("pick", params.name))

    observer = new ResizeObserver(() => myChart?.resize())
    observer.observe(chart.value)
  } catch (e) {
    console.error("加载品类数据失败", e)
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
