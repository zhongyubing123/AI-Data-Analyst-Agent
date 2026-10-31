# 2. 启动服务

## 2.1 装依赖

```bash
cd C:\Users\zhong\Desktop\AI-Data-Analyst-Agent\ai-service
conda activate ai-agent
pip install -r requirements.txt
```

## 2.2 配 .env

`ai-service/.env`：

```ini
DEEPSEEK_API_KEY=sk-xxxx
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=你的密码
MYSQL_DATABASE=ecommerce
```

Redis 默认 `localhost:6379`，改端口去 `services/redis_client.py`。

## 2.3 起服务

```bash
cd ai-service
uvicorn app:app --reload
```

## 2.4 试问

```powershell
$body = '{"message":"销售额最高的五个品牌"}'
Invoke-RestMethod -Uri http://127.0.0.1:8000/chat -Method Post -Body $body -ContentType "application/json"
```

期望：`answer` 里出现品牌名和金额。

再试三条，覆盖查数、画图、知识问答：

```powershell
$list = @(
  "销量前十的商品",
  "生成品牌销售额柱状图",
  "buy_count 是什么意思"
)
foreach ($m in $list) {
  $b = @{message = $m} | ConvertTo-Json -Compress
  Invoke-RestMethod -Uri http://127.0.0.1:8000/chat -Method Post -Body $b -ContentType "application/json"
}
```

第三条应该返回 `chart` 字段，里面有 `title`、`xAxis`、`yAxis`、`series`。

报错先看 `ai-service/logs/` 下最新的 `trace_*.json`，里面有 `sql` 和 `error`。

## 2.5 常见安装问题

`pip install faiss-cpu` 在 Windows 上偶尔失败：

```bash
conda install -c conda-forge faiss-cpu
```

首次跑检索会下载 all-MiniLM-L6-v2（约 90MB），提前跑一次让模型进本地缓存：

```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

知识库改过之后要重建索引，否则检索还是旧内容：

```bash
python -m services.build_vector
```
