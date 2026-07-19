import axios from "axios";

const ai = axios.create({
  baseURL: "http://127.0.0.1:8000",
  timeout: 30000,
});

export function chat(message) {
  return ai.post("/chat", {
    message,
  });
}