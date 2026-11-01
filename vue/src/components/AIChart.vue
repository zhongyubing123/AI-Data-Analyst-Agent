<template>
  <div ref="chartRef" class="ai-chart"></div>
</template>

<script setup>
import * as echarts from "echarts";
import { ref, onMounted, onBeforeUnmount, watch } from "vue";

const props = defineProps({
  option: {
    type: Object,
    required: true
  }
});

const chartRef = ref(null);
let chart = null;
let observer = null;

// 模型给的配置直接渲染时，横轴标签容易被自动隐藏，这里补一层默认值
const withDefaults = (option) => {
  const opt = JSON.parse(JSON.stringify(option));

  if (opt.xAxis && !Array.isArray(opt.xAxis)) {
    opt.xAxis.axisLabel = {
      interval: 0,
      rotate: 30,
      fontSize: 11,
      ...(opt.xAxis.axisLabel || {})
    };
  } else if (Array.isArray(opt.xAxis)) {
    opt.xAxis = opt.xAxis.map(axis => ({
      ...axis,
      axisLabel: {
        interval: 0,
        rotate: 30,
        fontSize: 11,
        ...(axis.axisLabel || {})
      }
    }));
  }

  opt.grid = {
    left: 60,
    right: 24,
    top: 60,
    bottom: 70,
    ...(opt.grid || {})
  };

  return opt;
};

const renderChart = () => {
  if (!chartRef.value || !props.option) return;

  if (!chart) {
    chart = echarts.init(chartRef.value);
  }

  chart.setOption(withDefaults(props.option), true);
};

onMounted(() => {
  renderChart();
  observer = new ResizeObserver(() => chart?.resize());
  observer.observe(chartRef.value);
});

onBeforeUnmount(() => {
  observer?.disconnect();
  chart?.dispose();
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

<style scoped>
.ai-chart {
  width: 100%;
  height: 400px;
}
</style>
