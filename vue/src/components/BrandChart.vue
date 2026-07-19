<template>
  <div ref="chart" style="width:100%;height:400px"></div>
</template>

<script setup>
import * as echarts from "echarts"
import { ref, onMounted, onBeforeUnmount } from "vue"
import axios from "axios"

const chart = ref(null)
let myChart = null

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

    window.addEventListener("resize", resizeChart)
  } catch (e) {
    console.error("加载品牌销售数据失败", e)
  }
})

const resizeChart = () => {
  myChart?.resize()
}

onBeforeUnmount(() => {
  window.removeEventListener("resize", resizeChart)
  myChart?.dispose()
})
</script>