curl -X POST 'http://localhost/v1/chat-messages' \
--header 'Authorization: Bearer app-OL7JwJk1d4pZc1ak8Bdgi3Ww' \
--header 'Content-Type: application/json' \
--data-raw '{
  "inputs": {},
  "query": "开始写",
  "response_mode": "streaming",
  "conversation_id": "",
  "user": "liujia"
}'