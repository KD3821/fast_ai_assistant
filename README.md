# fast_ai_assistant

<h1 align="center">AI assistant (RAG) based on <a href="https://stochasticcoder.com/2024/05/05/empower-your-ai-agent-with-azure-cosmos-db/">Jonathan Scholtes's article</a></h1>
<p align="center"><img src="https://img.shields.io/badge/made_by-KD3821-crimson"></p><br>

<p align="center"><img src="https://github.com/kd3821/fast_ai_assistant/blob/main/img/DALLE_cruiseship.png?raw=true"></p>

<p align="center">Service for booking cruises with the help of AI assistant (LangChain & FastAPI & MongoDB+ChromaDB)</p>

Instructions:
<ul>
<li>OpenAI and LangChain(LangSmith) API keys required to run the service</li>
<li>Files "ships.json" and "destinations.json" contain "cruise data" which will be used to build cruise itineraries (check "ships_destinations" dir)</li>
<li>For MongoDB the service uses a Docker image without AVX support (switch to appropriate if needed)</li>
<li>Instead of using MongoDB Atlas Vector Search the service uses ChromaDB for vectorized documents storage</li>
<li>As for UI it is possible to use FastAPI's build-in SwaggerUI page to make HTTP requests</li>
<li>For WebSocket requests it is possible to use "Web Socket Client" extension for Google Chrome browser</li>
<li>Service is not fully dockerized yet: FastAPI service have to be started separately</li>
<li>Create and fill-in the .env file in base directory (follow the 'env.example' file)</li>
<li>Start docker network with command:<br>CURRENT_UID=0:0 docker-compose -f docker-compose.yml up</li>
<li>After MongoDB and RabbitMQ containers are up and ready to accept connections<br>
then start FastAPI service with command: python3 -m src.main</li>
<li>In web-browser open page: "http://127.0.0.1:8088/docs" and in section "Data Storage" upload "cruise_data"
via sending POST request on:<br>"http://127.0.0.1:8088/storage/cruises-upload" including ships.json and destinations.json files</li>
<li>After that all the "cruise data" is loaded into MongoDB and ChromaDB databases</li>
<li>Service can be used via HTTP protocol or WebSocket protocol:<br>
HTTP: sending POST requests to "http://127.0.0.1:8088/prompts/travel-agent"<br>
WebSocket: connecting to "ws://localhost:8088/prompts/travel-chat"</li>
<li>Sending HTTP POST request require to send unique "session_id" along with "text" in body of request<br>
It can be easily obtained via HTTP GET request to "http://127.0.0.1:8088/prompts/session-id"</li>
<li>Connecting via WebSocket protocol replies with "Session_id" header holding "session_id string"<br>
It must be sent along with "text" data in the body of every ws-request to the service</li>
<li>"Session_id" helps service to identify dialog and keeps track of it's history<br>
That is why it's recommended to store it on the "client" till the end of the dialog</li>
<li>If WebSocket connection was closed for any reason it is possible to restore it by adding
<br>query param to url "ws://localhost:8088/prompts/travel-chat?session_id=XXXXXXXXX" during reconnect</li>
<li>History of every dialog will be stored in "history" collection of MongoDB</li>
<li>All requests can be monitored in LangSmith service</li>
</ul>
<p align="center"><img src="https://github.com/kd3821/fast_ai_assistant/blob/main/img/upload_json_data.png?raw=true"></p>
<p align="center"><img src="https://github.com/kd3821/fast_ai_assistant/blob/main/img/swagger_ui_travel_chat.png?raw=true"></p>
<p align="center"><img src="https://github.com/kd3821/fast_ai_assistant/blob/main/img/swagger_ui_response.png?raw=true"></p>
<p align="center"><img src="https://github.com/kd3821/fast_ai_assistant/blob/main/img/ws_travel_chat.png?raw=true"></p>
<p align="center"><img src="https://github.com/kd3821/fast_ai_assistant/blob/main/img/lang_smith.png?raw=true"></p>

<p align="center">Thanks for visiting!</p>
<p align="center">And Big Kudos to <a href="https://stochasticcoder.com/">Jonathan Scholtes and his blog</a> for helping to implement first RAG app.</p>
<br>
<br>
<p align="center">It's working!🚀</p>
<p align="center"><img src="https://github.com/kd3821/fast_ai_assistant/blob/main/img/DS_flask_app.jpeg?raw=true"></p>