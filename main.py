from fastapi import FastAPI, WebSocket
import pyperclip
import uvicorn
from threading import Thread
import time
import asyncio

app = FastAPI()

# 存储所有连接的 WebSocket 客户端
connected_clients = set()

# 存储剪贴板内容
clipboard_content = ""

# WebSocket 路由
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            # 接收客户端消息（如果需要双向通信）
            data = await websocket.receive_text()
            print(f"Received from client: {data}")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        connected_clients.remove(websocket)

# 剪贴板监听函数
def clipboard_listener():
    global clipboard_content
    while True:
        new_content = pyperclip.paste()
        if new_content != clipboard_content:
            clipboard_content = new_content
            print(f"Clipboard changed: {clipboard_content}")
            # 广播剪贴板内容到所有连接的客户端
            if connected_clients:
                for client in connected_clients:
                    asyncio.run(client.send_text(clipboard_content))
        time.sleep(1)  # 每秒检查一次剪贴板

# 启动剪贴板监听线程
Thread(target=clipboard_listener, daemon=True).start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)