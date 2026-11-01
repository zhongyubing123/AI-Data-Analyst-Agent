<template>
  <div class="chat-container">
    <h2>Enterprise AI Data Analysis Agent</h2>

    <div class="chat-box" ref="box">
      <div
        v-for="(item,index) in messages"
        :key="index"
        class="message"
      >
        <div v-if="item.role==='user'" class="user">
          👤用户： {{ item.content }}
        </div>

        <div v-else class="assistant">
          🤖助手： {{ item.content }}

          <AIChart
            v-if="item.chart"
            :option="item.chart"
          />

          <details v-if="item.sql" class="evidence">
            <summary>依据：{{ item.rows }} 行数据</summary>
            <pre>{{ item.sql }}</pre>
          </details>
        </div>
      </div>

      <div v-if="loading" class="assistant loading">正在查询…</div>
    </div>

    <div class="examples">
      <button
        v-for="text in examples"
        :key="text"
        @click="fill(text)"
      >
        {{ text }}
      </button>
    </div>

    <div class="input-box">
      <input
        v-model="question"
        @keyup.enter="sendMessage"
        placeholder="请输入问题，例如：哪个品类卖得最好"
      />

      <button @click="sendMessage" :disabled="loading">
        发送
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from "vue"
import axios from "axios"
import AIChart from "../components/AIChart.vue"

const question = ref("")
const messages = ref([])
const loading = ref(false)
const box = ref(null)

const examples = [
  "哪个品类卖得最好",
  "浏览多但买得少的商品",
  "给点运营建议"
]

const fill = (text) => {
  question.value = text
}

const scrollBottom = async () => {
  await nextTick()
  if (box.value) {
    box.value.scrollTop = box.value.scrollHeight
  }
}

const sendMessage = async () => {
  if (!question.value.trim() || loading.value) return

  const text = question.value

  messages.value.push({ role: "user", content: text })

  question.value = ""
  loading.value = true
  scrollBottom()

  try {
    const res = await axios.post(
      "http://127.0.0.1:8000/chat",
      { message: text },
      { timeout: 60000 }
    )

    messages.value.push({
      role: "assistant",
      content: res.data.answer,
      chart: res.data.chart,
      sql: res.data.sql,
      rows: res.data.rows
    })
  } catch (e) {
    messages.value.push({
      role: "assistant",
      content: "请求失败，检查服务是否启动：" + (e.message || "")
    })
  } finally {
    loading.value = false
    scrollBottom()
  }
}
</script>

<style scoped>
.chat-container {
  width: 900px;
  margin: 30px auto;
}

.chat-box {
  height: 600px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  overflow-y: auto;
  padding: 20px;
}

.message {
  margin-bottom: 20px;
}

.user {
  text-align: right;
  color: #6cb6ff;
}

.assistant {
  color: inherit;
  line-height: 1.8;
}

.loading {
  opacity: 0.6;
}

.evidence {
  margin-top: 8px;
  font-size: 12px;
  opacity: 0.65;
}

.evidence summary {
  cursor: pointer;
  user-select: none;
}

.evidence pre {
  white-space: pre-wrap;
  word-break: break-all;
  margin: 6px 0 0;
  padding: 8px;
  border-left: 2px solid rgba(255, 255, 255, 0.3);
  font-family: Consolas, monospace;
}

.examples {
  display: flex;
  gap: 8px;
  margin-top: 12px;
  flex-wrap: wrap;
}

.examples button {
  width: auto;
  padding: 4px 12px;
  font-size: 12px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.25);
  background: transparent;
  color: inherit;
  cursor: pointer;
}

.input-box {
  display: flex;
  margin-top: 12px;
}

input {
  flex: 1;
  padding: 10px;
}

button {
  width: 100px;
}
</style>
