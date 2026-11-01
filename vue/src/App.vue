<template>
  <div class="app">
    <header class="topbar">
      <span class="title">电商数据分析助手</span>
      <span class="tip">点击图表上的元素，名字会带进右侧输入框</span>
    </header>

    <main class="body">
      <section class="left">
        <Dashboard @pick="onPick" />
      </section>

      <aside class="right">
        <Chat :draft="draft" @used="draft = ''" />
      </aside>
    </main>
  </div>
</template>

<script setup>
import { ref } from "vue"
import Chat from "./views/Chat.vue"
import Dashboard from "./views/Dashboard.vue"

const draft = ref("")

const onPick = (name) => {
  draft.value = name
}
</script>

<style scoped>
.app {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.topbar {
  height: 52px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 20px;
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

.body {
  flex: 1;
  display: flex;
  min-height: 0;
}

.left {
  flex: 1;
  min-width: 0;
  padding: 16px;
  overflow: auto;
}

.right {
  width: 400px;
  flex-shrink: 0;
  border-left: 1px solid rgba(255, 255, 255, 0.15);
  display: flex;
  flex-direction: column;
  min-height: 0;
}

@media (max-width: 1200px) {
  .body {
    flex-direction: column;
  }

  .right {
    width: auto;
    height: 55%;
    border-left: none;
    border-top: 1px solid rgba(255, 255, 255, 0.15);
  }
}
</style>
