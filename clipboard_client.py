import asyncio
import pyperclip
import websockets

clipboard_content = ""


async def connect_to_server(uri):
    global clipboard_content
    async with websockets.connect(uri) as websocket:
        # 发送本地剪贴板内容到服务端
        local_content = pyperclip.paste()
        await websocket.send(local_content)

        # 启动一个任务来监听服务端消息
        receive_task = asyncio.create_task(receive_messages(websocket))
        # 启动一个任务来监听本地剪贴板变化
        clipboard_task = asyncio.create_task(clipboard_listener(websocket))

        await asyncio.gather(receive_task, clipboard_task)


async def receive_messages(websocket):
    global clipboard_content
    try:
        while True:
            data = await websocket.recv()
            print(f"Received from server: {data}")
            if data != clipboard_content:
                clipboard_content = data
                pyperclip.copy(data)  # 将接收到的数据复制到本地剪贴板
    except Exception as e:
        print(f"Error receiving messages: {e}")


async def clipboard_listener(websocket):
    global clipboard_content
    while True:
        new_content = pyperclip.paste()
        if new_content != clipboard_content:
            clipboard_content = new_content
            print(f"Clipboard changed: {clipboard_content}")
            await websocket.send(clipboard_content)
        await asyncio.sleep(1)


if __name__ == "__main__":
    # 提示用户输入 IP 和端口，并提供默认值
    address = input("请输入 WebSocket 服务器地址（格式为 ip:port，默认为 localhost:8001）：").strip()

    # 如果用户输入了内容，则解析；否则使用默认值
    if address:
        try:
            ip, port = address.split(":")
            uri = f"ws://{ip}:{port}/ws"
        except ValueError:
            print("输入格式错误，将使用默认值。")
            uri = "ws://localhost:8001/ws"
    else:
        uri = "ws://localhost:8001/ws"

    print(f"正在连接到 WebSocket 服务器：{uri}")
    asyncio.run(connect_to_server(uri))