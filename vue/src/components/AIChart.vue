<template>
  <div ref="chartRef" style="width:100%;height:400px;"></div>
</template>

<script setup>
import * as echarts from "echarts";
import { ref, onMounted, watch } from "vue";

const props = defineProps({
  option: {
    type: Object,
    required: true
  }
});

const chartRef = ref(null);
let chart = null;

const renderChart = () => {
  if (!chartRef.value || !props.option) return;

  if (!chart) {
    chart = echarts.init(chartRef.value);
  }

  chart.setOption(props.option, true);
};

onMounted(() => {
  renderChart();
});

watch(
  () => props.option,
  () => {
    renderChart();
  },
  {
    deep: true
  }
);
</script>