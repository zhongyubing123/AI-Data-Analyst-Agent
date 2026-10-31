<template>
  <div>
    <div class="tabs">
      <button :class="{ active: view === 'chat' }" @click="view = 'chat'">
        智能问答
      </button>
      <button :class="{ active: view === 'board' }" @click="view = 'board'">
        数据看板
      </button>
    </div>

    <Chat v-if="view === 'chat'" />
    <Dashboard v-else />
  </div>
</template>

<script setup>
import { ref } from "vue"
import Chat from "./views/Chat.vue"
import Dashboard from "./views/Dashboard.vue"

const view = ref("chat")
</script>

<style scoped>
.tabs {
  display: flex;
  gap: 8px;
  padding: 12px 16px 0;
}

.tabs button {
  padding: 6px 16px;
  border: 1px solid #444;
  background: transparent;
  color: #bbb;
  border-radius: 4px;
  cursor: pointer;
}

.tabs button.active {
  background: #409eff;
  border-color: #409eff;
  color: #fff;
}
</style>
