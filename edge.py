import asyncio
from EdgeGPT import Chatbot

async def main():
    bot = Chatbot(cookiePath="cookies.json")
    print(await bot.ask(prompt="write several haikus about birbs flying in the skai above"))
    await bot.close()


if __name__ == "__main__":
    asyncio.run(main())
