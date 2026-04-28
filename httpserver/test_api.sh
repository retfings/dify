#!/bin/bash

BASE_URL="http://localhost:7890"

echo "=========================================="
echo "  Key-Value Storage API 测试脚本"
echo "=========================================="
echo ""

echo "1️⃣  测试写入数据 - 创建新 key"
echo "-------------------------------------------"
curl -s -X POST "${BASE_URL}/write" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "username",
    "value": "dify"
  }' | jq .

echo ""
echo "2️⃣  测试写入数据 - 创建第二个 key"
echo "-------------------------------------------"
curl -s -X POST "${BASE_URL}/write" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "email",
    "value": "user@example.com"
  }' | jq .

echo ""
echo "3️⃣  测试读取数据 - username"
echo "-------------------------------------------"
curl -s -X POST "${BASE_URL}/read" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "username"
  }' | jq .

echo ""
echo "4️⃣  测试读取数据 - email"
echo "-------------------------------------------"
curl -s -X POST "${BASE_URL}/read" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "email"
  }' | jq .

echo ""
echo "5️⃣  测试更新数据 - 更新已存在的 key"
echo "-------------------------------------------"
curl -s -X POST "${BASE_URL}/write" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "username",
    "value": "admin"
  }' | jq .

echo ""
echo "6️⃣  测试读取数据 - 验证更新后的值"
echo "-------------------------------------------"
curl -s -X POST "${BASE_URL}/read" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "username"
  }' | jq .

echo ""
echo "7️⃣  测试读取数据 - 读取不存在的 key"
echo "-------------------------------------------"
curl -s -X POST "${BASE_URL}/read" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "notfound"
  }' | jq .

echo ""
echo "8️⃣  测试写入数据 - 包含特殊字符的值"
echo "-------------------------------------------"
curl -s -X POST "${BASE_URL}/write" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "config",
    "value": "{\"theme\": \"dark\", \"language\": \"zh-CN\"}"
  }' | jq .

echo ""
echo "9️⃣  测试读取数据 - 读取特殊字符的值"
echo "-------------------------------------------"
curl -s -X POST "${BASE_URL}/read" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "config"
  }' | jq .

echo ""
echo "=========================================="
echo "  测试完成"
echo "=========================================="
echo ""
echo "📋 完整的日志文件请查看: app.log"
echo "📋 数据存储文件请查看: data.json"
echo ""
