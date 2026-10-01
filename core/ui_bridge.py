import asyncio
import threading

from websockets.asyncio.server import serve


class UIBridge:

    def __init__(self):

        self.clients = set()

        self.loop = None
        self.thread = None

    async def handler(self, websocket):

        self.clients.add(websocket)

        print("JARVIS UI connected.")

        try:

            await websocket.wait_closed()

        finally:

            self.clients.discard(websocket)

            print("JARVIS UI disconnected.")

    async def start_server(self):

        self.loop = asyncio.get_running_loop()

        async with serve(
            self.handler,
            "localhost",
            8765
        ):

            print(
                "JARVIS UI Bridge online: "
                "ws://localhost:8765"
            )

            await asyncio.Future()

    def start(self):

        def run_server():

            asyncio.run(
                self.start_server()
            )

        self.thread = threading.Thread(
            target=run_server,
            daemon=True
        )

        self.thread.start()

    async def _send(self, message):

        if not self.clients:
            return

        disconnected = set()

        for client in self.clients:

            try:

                await client.send(message)

            except Exception:

                disconnected.add(client)

        self.clients.difference_update(
            disconnected
        )

    def send(self, message):

        if self.loop is None:
            print(
                "JARVIS UI Bridge is not running."
            )
            return

        asyncio.run_coroutine_threadsafe(
            self._send(message),
            self.loop
        )

    def turn_on(self):

        print("UI COMMAND → TURN ON")

        self.send("turn_on")

    def turn_off(self):

        print("UI COMMAND → TURN OFF")

        self.send("turn_off")

    def speaking(self):

        print("UI COMMAND → SPEAKING")

        self.send("speaking")

    def idle(self):

        print("UI COMMAND → IDLE")

        self.send("idle")