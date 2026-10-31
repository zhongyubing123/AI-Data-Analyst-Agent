<template>
  <div class="chat-container">
    <h2>Enterprise AI Data Analysis Agent</h2>

    <div class="chat-box">
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
        </div>
      </div>
    </div>

    <div class="input-box">
      <input
        v-model="question"
        @keyup.enter="sendMessage"
        placeholder="请输入问题"
      />

      <button @click="sendMessage">
        发送
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import axios from "axios"
import AIChart from "../components/AIChart.vue"

const question = ref("")
const messages = ref([])

const sendMessage = async () => {
  if (!question.value.trim()) return

  const text = question.value

  messages.value.push({
    role: "user",
    content: text
  })

  question.value = ""

  const res = await axios.post(
    "http://127.0.0.1:8000/chat",
    { message: text }
  )

  messages.value.push({
    role: "assistant",
    content: res.data.answer,
    chart: res.data.chart
  })
}
</script>

<style scoped>
.chat-container{
  width:900px;
  margin:30px auto;
}

.chat-box{
  height:600px;
  border:1px solid #ddd;
  overflow-y:auto;
  padding:20px;
}

.message{
  margin-bottom:20px;
}

.user{
  text-align:right;
  color:#409EFF;
}

.assistant{
  color:#333;
}

.input-box{
  display:flex;
  margin-top:20px;
}

input{
  flex:1;
  padding:10px;
}

button{
  width:100px;
}
</style>