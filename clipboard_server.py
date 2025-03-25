import time
from fastapi import FastAPI, WebSocket
import pyperclip
import uvicorn
import asyncio
from threading import Thread
import socket

def get_ipv4_address():
    try:
        # 创建一个 UDP socket，连接到公共地址（不实际发送数据）
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # 使用 Google 的公共 DNS 地址
            ip = s.getsockname()[0]  # 获取本地 IP 地址
        return ip
    except Exception as e:
        print(f"无法获取 IPv4 地址: {e}")
        return None
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
    # 提示用户输入 IP 和端口，并提供默认值
    address = input("请输入 IP 和端口（格式为 ip:port，默认为 0.0.0.0:8001）：").strip()

    # 如果用户输入了内容，则解析；否则使用默认值
    if address:
        try:
            ip, port = address.split(":")
            port = int(port)  # 确保端口是整数
        except ValueError:
            print("输入格式错误，将使用默认值。")
            ip, port = "0.0.0.0", 8001
    else:
        ip, port = "0.0.0.0", 8001

    if ip == "0.0.0.0":
        ip = get_ipv4_address()
    print(f"已复制服务端地址：{ip}:{port}")
    pyperclip.copy(f"{ip}:{port}")
    Thread(target=clipboard_listener, daemon=True).start()
    uvicorn.run(app, host=ip, port=int(port))