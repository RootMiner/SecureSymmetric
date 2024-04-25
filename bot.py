# upload and download enc file on discord server using token

import os
from dotenv import load_dotenv
import discord
from time import sleep
from multiprocessing import Process

def uploadFile(file_path):
  # connecting discord bot
  load_dotenv()
  # print(file_path); exit()
  if os.getenv('DISCORD_TOKEN') == None: # you need to create your own bot, follow the guidance in README.md
    bot_token = input("enter your discord bot token: ")
    with open('.env', "w") as env_file:
      env_file.write('DISCORD_TOKEN="' + bot_token + '"\n')
    load_dotenv()
  
  TOKEN = os.getenv('DISCORD_TOKEN')

  if os.getenv('DISCORD_CHANNEL') == None: # channel id, developer option needs to be enabled
    channel_id = input("enter your_channel id: ")
    with open('.env', "a") as env_file:
      env_file.write('DISCORD_CHANNEL="' + channel_id + '"\n')
    load_dotenv()

  intents = discord.Intents.all()
  client = discord.Client(intents=intents)

  # uploading file
  @client.event
  async def on_ready():
    print(f'{client.user} has connected to Discord!')
    channel = await client.fetch_channel(os.getenv('DISCORD_CHANNEL'))
    await channel.send(file=discord.File(file_path)) # file uploading here
    print('file uploaded on discord successfully!')

  # executing bot and turning it back off after 10 seconds
  def run(): client.run(TOKEN)
  process = Process(target=run)
  process.start()
  sleep(10)
  process.terminate()

if __name__ == "__main__":
  uploadFile()