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

curl -X POST \
  http://127.0.0.1:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Ciao! Puoi aiutarmi con la mia dieta?",
    "user": {
      "Customer_ID": "test-user-id-123",
      "Name": "Francesco",
      "Surname": "Roveda",
      "Age": 23,
      "Sesso": 1,
      "Weight": 134,
      "Height": 152,
      "PercentualeMassaGrassa": 27,
      "DispendioCalorico": 1.58,
      "DietType": 1,
      "Macroblocco": 0,
      "Week": 0,
      "Day": 1,
      "DistrettoCarente1": null,
      "DistrettoCarente2": null,
      "ExerciseSelected": true,
      "Contry": "Italia",
      "City": "Milano",
      "Province": "MI",
      "subExpire": "2022-12-31",
      "SubType": 0,
      "Kcal": 3734,
      "Fats": 87,
      "Proteins": 308,
      "Carbs": 430,
      "SettimanaTestEsercizi": true,
      "SettimanaTestPesi": false,
      "WorkoutDellaSettimna": {
        "1": [
          {
            "Tipologia": "QUADRICIPITI",
            "Name": "PRESSA 45°",
            "Ripetizioni": "9",
            "Serie": 3,
            "Peso": 30,
            "Riposo": 90,
            "Note": "Rispetta il peso indicato",
            "DistrettoText": false
          }
        ]
      }
    }
  }'
