import time
from fastapi import FastAPI, WebSocket
import pyperclip
import uvicorn
import asyncio
from threading import Thread

app = FastAPI()
connected_clients = set()
clipboard_content = ""


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received from client: {data}")
            pyperclip.copy(data)  # 将接收到的数据复制到本地剪贴板
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        connected_clients.remove(websocket)


async def broadcast_content(content):
    tasks = []
    for client in connected_clients:
        try:
            task = client.send_text(content)
            tasks.append(task)
        except Exception as e:
            print(f"Error sending to client: {e}")
    if tasks:
        await asyncio.gather(*tasks)


def clipboard_listener():
    global clipboard_content
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    while True:
        new_content = pyperclip.paste()
        if new_content != clipboard_content:
            clipboard_content = new_content
            print(f"Clipboard changed: {clipboard_content}")
            if connected_clients:
                loop.run_until_complete(broadcast_content(clipboard_content))
        time.sleep(1)


if __name__ == "__main__":
    # address = input("请输入ip和端口:")
    # ip, port = address.split(":")
    port = 8001
    ip = "192.168.31.194"
    Thread(target=clipboard_listener, daemon=True).start()
    uvicorn.run(app, host=ip, port=int(port))