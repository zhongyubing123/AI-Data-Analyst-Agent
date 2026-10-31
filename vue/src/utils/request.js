import axios from "axios";

// 看板接口现在也由 FastAPI 提供，和对话同一个服务
const request = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
  timeout: 10000,
});

export default request;
