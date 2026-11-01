<template>
  <div class="app">
    <header class="topbar">
      <span class="title">电商数据分析助手</span>
      <span class="tip">直接提问，或点击图表上的元素把名字带进输入框</span>
    </header>

    <main class="main">
      <Chat />
    </main>
  </div>
</template>

<script setup>
import Chat from "./views/Chat.vue"
</script>

<style scoped>
.app {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.topbar {
  height: 52px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
}

.title {
  font-size: 16px;
  font-weight: 600;
}

.tip {
  font-size: 12px;
  opacity: 0.6;
}

.main {
  flex: 1;
  min-height: 0;
  overflow: hidden;
}
</style>
