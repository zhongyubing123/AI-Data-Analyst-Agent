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

onMounted(async () => {
  try {
    const { data } = await axios.get("/api/brand/sales")

    myChart = echarts.init(chart.value)

    myChart.setOption({
      title: {
        text: "品牌销售占比"
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
          data: data.map(item => ({
            name: item.brand,
            value: item.salesAmount
          }))
        }
      ]
    })

    myChart.on("click", (params) => emit("pick", params.name))

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
