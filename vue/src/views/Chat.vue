<template>
  <div class="chat-container">
    <div class="chat-box" ref="box">
      <div
        v-for="(item,index) in messages"
        :key="index"
        class="message"
      >
        <div v-if="item.role==='user'" class="user">
          👤 {{ item.content }}
        </div>

        <div v-else class="assistant">
          🤖 {{ item.content }}

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
        @click="question = text"
      >
        {{ text }}
      </button>
    </div>

    <div class="input-box">
      <input
        v-model="question"
        @keyup.enter="sendMessage"
        placeholder="问点什么，比如：哪个品牌客单价最高"
      />

      <button @click="sendMessage" :disabled="loading">
        发送
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from "vue"
import axios from "axios"
import AIChart from "../components/AIChart.vue"

const props = defineProps({
  draft: { type: String, default: "" }
})

const emit = defineEmits(["used"])

const question = ref("")
const messages = ref([])
const loading = ref(false)
const box = ref(null)

const examples = [
  "哪个品类卖得最好",
  "哪个品牌客单价最高",
  "给点运营建议"
]

// 点图带进来的名字，填进输入框，不自动发送
watch(
  () => props.draft,
  (value) => {
    if (value) {
      question.value = value
      emit("used")
    }
  }
)

const scrollBottom = async () => {
  await nextTick()
  if (box.value) {
    box.value.scrollTop = box.value.scrollHeight
  }
}

// 服务重启或瞬时断连时重试一次
const postChat = async (text, retry = true) => {
  try {
    return await axios.post(
      "http://127.0.0.1:8000/chat",
      { message: text },
      { timeout: 60000 }
    )
  } catch (e) {
    if (retry) {
      await new Promise(r => setTimeout(r, 800))
      return postChat(text, false)
    }
    throw e
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
    const res = await postChat(text)

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
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
  padding: 12px 16px 16px;
  box-sizing: border-box;
}

.chat-box {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding-right: 6px;
}

.message {
  margin-bottom: 14px;
  font-size: 14px;
}

.user {
  text-align: right;
  color: #6cb6ff;
}

.assistant {
  color: inherit;
  line-height: 1.7;
}

.loading {
  opacity: 0.6;
}

.evidence {
  margin-top: 6px;
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
  gap: 6px;
  margin: 8px 0;
  flex-wrap: wrap;
}

.examples button {
  width: auto;
  padding: 3px 10px;
  font-size: 12px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.25);
  background: transparent;
  color: inherit;
  cursor: pointer;
}

.input-box {
  display: flex;
  gap: 8px;
}

input {
  flex: 1;
  padding: 8px;
  min-width: 0;
}

.input-box button {
  width: 72px;
  flex-shrink: 0;
}
</style>
