# Key-Value Storage Server

基于 FastAPI 的轻量级键值存储服务，同时支持 SQLite 数据库和 JSON 文件持久化。

## 功能特性

- **双端存储**：数据同时保存到 SQLite 数据库和 JSON 文件
- **线程安全**：使用文件锁保证并发访问安全
- **RESTful API**：提供简洁的 POST 接口
- **自动初始化**：启动时自动创建数据库表和 JSON 文件
- **企业级日志**：完整的请求追踪、错误日志、性能监控

## 技术栈

- **FastAPI**: Web 框架
- **SQLAlchemy**: ORM 框架
- **SQLite**: 关系型数据库
- **Pydantic**: 数据验证
- **Python Logging**: 企业级日志系统

## 日志系统

系统集成了完整的企业级日志功能：

### 日志特性

- **双通道输出**：同时输出到控制台和日志文件
- **请求追踪**：每个请求分配唯一 Request ID
- **性能监控**：记录每个请求的处理时间
- **错误追踪**：完整的异常堆栈信息
- **分级日志**：INFO、WARNING、ERROR、CRITICAL

### 日志文件

日志同时输出到两个位置：

- **控制台**：`stdout` 实时显示
- **文件**：`app.log` 持久化存储

### 日志格式

```
2026-04-28 10:30:45 | INFO     | kv-storage:startup_event:48 | Application startup initiated
2026-04-28 10:30:45 | INFO     | kv-storage:startup_event:52 | Database: sqlite:///./storage.db
2026-04-28 10:31:20 | INFO     | kv-storage:log_requests:78 | [1234567890] --> POST /write
2026-04-28 10:31:20 | INFO     | kv-storage:write_key_value:141 | Write operation initiated: key='username'
2026-04-28 10:31:20 | INFO     | kv-storage:write_key_value:150 | Creating new key: 'username'
2026-04-28 10:31:20 | INFO     | kv-storage:write_key_value:159 | Database commit successful
2026-04-28 10:31:20 | INFO     | kv-storage:log_requests:93 | [1234567890] <-- POST /write status=200
```

### 响应头信息

每个响应都会包含以下头信息：

- **X-Request-ID**: 请求唯一标识符
- **X-Process-Time**: 请求处理时间（毫秒）

## 安装

```bash
cd httpserver
pip install -r requirements.txt
```

## 运行服务

```bash
python server.py
```

默认端口: `7890`

### 命令行参数

```bash
python server.py --help
```

可用参数：

- `-p, --port`: 服务器端口（默认: 7890）
- `--host`: 服务器地址（默认: 0.0.0.0）

### 使用示例

```bash
# 使用默认端口 7890
python server.py

# 指定端口
python server.py -p 8080

# 指定端口和地址
python server.py --host 127.0.0.1 --port 9000
```

服务启动后访问 `http://localhost:7890`

- API 文档: `http://localhost:7890/docs`
- 交互式调试界面: `http://localhost:7890/redoc`

## API 端点

### 写入数据

**POST** `/write`

写入或更新键值对，同时保存到 SQLite 和 JSON 文件。

**请求示例：**

```bash
curl -X POST "http://localhost:7890/write" \
  -H "Content-Type: application/json" \
  -d '{"key": "username", "value": "dify"}'
```

**请求体：**

```json
{
  "key": "string",
  "value": "string"
}
```

**响应示例：**

```json
{
  "status": "success",
  "message": "Key 'username' saved successfully"
}
```

### 读取数据

**POST** `/read`

从 JSON 文件读取指定键的值。

**请求示例：**

```bash
curl -X POST "http://localhost:7890/read" \
  -H "Content-Type: application/json" \
  -d '{"key": "username"}'
```

**请求体：**

```json
{
  "key": "string"
}
```

**响应示例：**

```json
{
  "key": "username",
  "value": "dify"
}
```

**错误响应 (404)：**

```json
{
  "detail": "Key 'notfound' not found"
}
```

## 数据存储

- **SQLite 数据库**: `storage.db`
- **JSON 文件**: `data.json`

JSON 文件格式示例：

```json
{
  "username": "dify",
  "email": "user@example.com"
}
```

## 项目结构

```
httpserver/
├── server.py         # 主程序
├── requirements.txt  # 依赖列表
├── test_api.sh       # Shell 测试脚本
├── test_api.py       # Python 测试脚本
├── storage.db        # SQLite 数据库（自动创建）
├── data.json         # JSON 数据文件（自动创建）
└── app.log           # 应用日志文件（自动创建）
```

## 测试

### Shell 脚本测试

```bash
# 启动服务器
python server.py

# 运行测试脚本
./test_api.sh
```

### Python 脚本测试

```bash
# 需要安装 requests 库
pip install requests

# 运行测试脚本
python test_api.py
```

## 注意事项

- 服务运行在 `0.0.0.0:8000`，可修改 `server.py` 中的端口
- JSON 文件用于快速读取，SQLite 用于结构化查询
- 写入操作会同时更新两个存储位置
- 读取操作仅从 JSON 文件读取
