import json
from src.discordrpc import DiscordRPC

with open('config.json', mode='rt', encoding='utf-8') as f:
    app = DiscordRPC(json.load(f))

app.start()
app.loop()
app.close()

