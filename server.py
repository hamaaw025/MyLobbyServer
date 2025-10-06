from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List

app = FastAPI()

# كل لعبة سيكون لها غرف متعددة
games: Dict[str, Dict[str, List[WebSocket]]] = {}

@app.get("/")
def root():
    return {"message": "Multigame Lobby Server is running 🚀"}

@app.websocket("/ws/{game_name}/{room_name}/{player_name}")
async def websocket_endpoint(websocket: WebSocket, game_name: str, room_name: str, player_name: str):
    await websocket.accept()
    # تجهيز القوائم
    if game_name not in games:
        games[game_name] = {}
    if room_name not in games[game_name]:
        games[game_name][room_name] = []

    # أضف اللاعب
    games[game_name][room_name].append(websocket)

    # إعلام الجميع بانضمام لاعب جديد
    for ws in games[game_name][room_name]:
        await ws.send_text(f"{player_name} joined {room_name} in {game_name}")

    try:
        while True:
            data = await websocket.receive_text()
            # بث الرسالة لكل من في الغرفة
            for ws in games[game_name][room_name]:
                await ws.send_text(f"{player_name}: {data}")

    except WebSocketDisconnect:
        # حذف اللاعب عند الخروج
        games[game_name][room_name].remove(websocket)
        for ws in games[game_name][room_name]:
            await ws.send_text(f"{player_name} left {room_name}")
