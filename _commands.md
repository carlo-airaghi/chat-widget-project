# Save Tree
'''bash
brew install tree
tree -L 2 > directory_tree.txt
'''

# Back-End
## Initilaize a new Node.js Project
```bash
npm init -y
```
## Install Dependencies
```bash
npm install express axios cors dotenv
```
- express: Web framework for Node.js.
- axios: Promise-based HTTP client for the browser and Node.js.
- cors: Middleware for enabling CORS (Cross-Origin Resource Sharing).
- dotenv: Loads environment variables from a .env file.
## Create Server File
```bash
touch server.js
```
Fill in the server file

## Handle environment variables
```bash
touch .env
```
Type in the openAPI product key

## Test the Backend 
```bash
node server.js
```
you should see: "Server is running on port 5000"
Use cURL to test the endpoint.
```bash
curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d '{"message": "Hello"}'
```
# Front-End
### Create Widget Directory
```bash
mkdir widget
```
### Create the Chat Widget
```bash
touch widget/chat-widget.js
```
Notes:

- The widget is wrapped in an Immediately Invoked Function Expression (IIFE) to avoid polluting the global namespace.
- Update the apiUrl variable with the actual URL of your backend server.
- The widget dynamically creates and styles its elements to minimize dependencies on the host website.


# Embed widget in website 
To embed the widget in a website, add the following script tag to the HTML of the host website:
```html
<script src="http://localhost:5000/chat-widget.js"></script>
```
- Create a test html under widget 
- Restart the server such that it starts serving test as well
```bash
node server.js
```

## Dockerization
```bash
docker build -t chat-widget-app .
```
```bash
docker run -d -p 5000:5000 \
  --env-file .env \
  --name chat-widget-container \
  chat-widget-app

```


## Adding web server with GPT
pip install torch transformers flask flask-cors
