from fastapi import FastAPI,Request,WebSocket,WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

PATH_TEMPLATES = r"C:\python\Agentic-models\Gemini\app\Frontend\templates"
PATH_STATIC = r"C:\python\Agentic-models\Gemini\app\Frontend\static"

app = FastAPI()
templates = Jinja2Templates(directory=PATH_TEMPLATES)
app.mount("/static", StaticFiles(directory=PATH_STATIC), name="static")


ANIMALS = [{"🐶": "🐱", "🐭":"🐹"}, {"🐰": "🦊","🐻": "🐼"} ,{"🐨": "🐯", "🦁": "🐮"}, {"🐷": "🐽", "🐸": "🐵"}, {"🙈": "🙉", "🙊":"🥪"}]
DOGS = [{"NAME": "🐶", "ANIMAL": "🐱"}, {"NAME": "🐭", "ANIMAL": "🐹"}, {"NAME": "🐰", "ANIMAL": "🦊"}, {"NAME": "🐻", "ANIMAL": "🐼"}, {"NAME": "🐨", "ANIMAL": "🐯"}, {"NAME": "🦁", "ANIMAL": "🐮"}, {"NAME": "🐷", "ANIMAL": "🐽"}, {"NAME": "🐸", "ANIMAL": "🐵"}, {"NAME": "🙈", "ANIMAL": "🙉"}, {"NAME": "🙊", "ANIMAL": "🥪"}]

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request,"DOGS":DOGS})

@app.websocket("/ws")
async def handle_websocket(websocket:WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            print(len(data))
    except WebSocketDisconnect:
        print("Sorry the Websocket has been disconnected...😒")


if __name__ == "__main__":
    uvicorn.run("Gemini_App:app",port=8000,host="0.0.0.0",reload=True)