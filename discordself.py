from pathlib import Path
import csv
from discord.ext import tasks
from datetime import datetime

import discord # discord.py-self

SERVER_ID = 000000000000000000

online_file = Path("online.csv")


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.server = None

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.background_online_members.start()

    async def get_online_members(self):
        members = await self.server.fetch_members()
        online_members = [
            member for member in members if member.status != discord.Status.offline
        ]
        return online_members

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        self.server = self.get_guild(SERVER_ID)
        print(f"Server: {self.server}")
        print("------")

    @tasks.loop(seconds=10)
    async def background_online_members(self):
        online_members = await self.get_online_members()
        num_online = len(online_members)
        print(f"Online members: {num_online}")

        with online_file.open("a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([current_date, num_online])

    @background_online_members.before_loop
    async def before_online_members(self):
        await self.wait_until_ready()  # wait until the bot logs in


client = MyClient()
client.run("XXXXXXXXXXXXXXXXXXXXXXXX.XXXXXX.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
