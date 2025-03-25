import time
import asyncio
from android import Android
import websockets

droid = Android()
clipboard_content = ""

async def connect_to_server(ip, port):
    global clipboard_content
    uri = f"ws://{ip}:{port}/ws"
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                # 监听剪贴板变化
                new_content = droid.getClipboard().result
                if new_content != clipboard_content:
                    if type(new_content) == str:
                        clipboard_content = new_content
                        print(f"Clipboard changed: {clipboard_content}")
                        await websocket.send(clipboard_content)

                # 接收服务器消息
                server_data = await asyncio.wait_for(websocket.recv(), timeout=1)
                if type(server_data) == str:
                    print(f"Received from server: {server_data}")
                    droid.setClipboard(server_data)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"Error: {e}")
                break


if __name__ == "__main__":
    # address = input("请输入服务器的ip和端口:")
    # ip, port = address.split(":")
    port = 8001
    ip = "192.168.31.194"
    asyncio.get_event_loop().run_until_complete(connect_to_server(ip, port))