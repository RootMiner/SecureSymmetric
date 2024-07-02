import os
import discord
from getpass import getpass
from platform import system
from dotenv import load_dotenv
from src.colors import S, E, A
from src.file_tweak import file_tweak

if   system() == 'Linux'  : separator = '/'
elif system() == 'Windows': separator = '\\'

def write_env_var():
  TOKEN   = getpass(f"\n[{A}] Enter your Discord Bot Token [hidden]: ")
  CHANNEL = input(f"[{A}] Enter your_channel id: ")

  with open('.env', "w") as env_file:
    env_file.write(f'DISCORD_TOKEN={TOKEN}')
    env_file.write(f'\nDISCORD_CHANNEL={CHANNEL}')

  return TOKEN, CHANNEL


# counts the maximum possible length of the file for spacing
def count_max_name_len(files_dict):
  max_file_name_len = 0
  for file_name, _ in files_dict.items():
    file_name_len = len(file_name)
    if file_name_len > max_file_name_len: 
      max_file_name_len = file_name_len
  return max_file_name_len


async def uploadFile(files_dict, is_remove): 
  load_dotenv()
  TOKEN = os.getenv('DISCORD_TOKEN')
  CHANNEL = os.getenv('DISCORD_CHANNEL')

  if TOKEN is None or CHANNEL is None: 
    TOKEN, CHANNEL = write_env_var()

  max_name_len = count_max_name_len(files_dict)

  intents = discord.Intents.all()
  client = discord.Client(intents=intents)

  @client.event
  async def on_ready():
    print(f"\n[{S}] {client.user} has connected to Discord!\n")
    channel = await client.fetch_channel(CHANNEL)
    for file_name, file_path in files_dict.items():
      await channel.send(file=discord.File(file_path))
      print(f"[{S}] {file_name.ljust(max_name_len)} uploaded on discord successfully")
      # this helps to directly remove enc_file from host
      _, mod_file_name = file_tweak(file_name, file_path.split(separator)[0], None)
      file_path = file_path.split(separator)[0]
      if is_remove:
        if input("do you want to delete " + mod_file_name + " [Y/n]: ") in ["", "y", "Y"]: os.remove(mod_file_name)
        else: pass
        if input("do you want to delete " + file_path + " [Y/n]: ") in ["", "y", "Y"]: os.remove(file_path)
        else: pass
    print(f"\n[-:-] Please do Ctrl + c to turn off the bot")

  try:
    await client.start(TOKEN)
    # await client.close() # --> this isn't working 
  except discord.errors.LoginFailure:
    await client.close()
    print(f"\n[{E}] Invalid TOKEN or Channel ID")
    write_env_var()
    await uploadFile(files_dict, is_remove)


if __name__ == '__main__':  uploadFile()

