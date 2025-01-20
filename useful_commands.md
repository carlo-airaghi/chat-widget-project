## Save Tree
```bash
brew install tree
tree -L 2 > directory_tree.txt
```

## Docker Build
```
docker build -t ai-chat-widget .
```

## Docker Run
```
docker run -d \                 
  --name ai-chat-widget \
  -p 5000:5000 \
  -e OPENAI_API_KEY=... \
  ai-chat-widget:latest
```

## Docker Hub
```
docker tag ai-chat-widget carloairaghi/chat-widget:latest
docker push carloairaghi/chat-widget:latest  
```

## Test API Call
```
curl http://localhost:5000/history/123
{"history":[]}
```
```
curl -X POST "http://localhost:8000/ask/" -H "Content-Type: application/json" -d '{"query": "What is the capital of France?"}'
```