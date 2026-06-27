import os
import asyncio
import discord
from discord.ext import commands
from aiohttp import web

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")


@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong ! Latence : {latency}ms")


async def healthcheck(request):
    return web.Response(text="OK")


async def start_healthcheck():
    app = web.Application()
    app.router.add_get("/", healthcheck)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Healthcheck server running on port {port}")


async def main():
    await start_healthcheck()
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise ValueError("La variable d'environnement DISCORD_TOKEN n'est pas définie")
    await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
