from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os
from bs4 import BeautifulSoup
from typing import List

# Load environment variables from the .env file
env_vars = dotenv_values(".env")
GroqAPIKey = ("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")

# Define CSS classes for parsing specific elements
classes = [
    "zCubwf", "hgKElc", "LTKOO SY7ric", "ZOLcW", "gsrt vk bk FzvwSb YwPhnf",
    "pclqee", "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "05uR6d LTKOO",
    "vl2Y6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikb48b gsrt",
    "sXLabe", "LWkfKe", "VQF4g", "qv3wpe", "kno-rdesc", "SPZz6b"
]

# Define a user-agent for making HTTP requests
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"

# Initialize the Groq client with the API key
client = Groq(api_key=GroqAPIKey)

# List to store chatbot messages
messages = []

# System message to provide context to the chatbot
SystemChatBot = {"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letters."}

# Function to perform a Google search
def GoogleSearch(Topic):
    search(Topic)
    return True  # Indicate success

# Function to generate content using AI and save it to a file
def Content(Topic):
    Topic = Topic.replace("Content", "")  # Remove "Content" from the topic
    ContentByAI = ContentWriterAI(Topic)  # Generate content using AI
    with open(f"Data/{Topic.lower().replace(' ', '_')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI)  # Write the content to the file
    OpenNotepad(f"Data/{Topic.lower().replace(' ', '_')}.txt")  # Open the file in Notepad
    return True  # Indicate success

# Function to open a file in Notepad
def OpenNotepad(File):
    default_text_editor = "notepad.exe"  # Default text editor
    subprocess.Popen([default_text_editor, File])  # Open the file in Notepad



# Function to generate content using the AI chatbot
def ContentWriterAI(prompt):
    messages.append({"role": "user", "content": prompt})  # Add the user prompt to messages
    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",  # Specify the AI model
        messages=[SystemChatBot] + messages,  # Include system instructions and chat history
        max_tokens=2048,  # Limit the maximum tokens in the response
        temperature=0.7,  # Adjust response randomness
        top_p=1,  # Control sampling for response diversity
        stream=True,  # Enable streaming response
        stop=None  # Allow the model to determine stopping conditions
    )
    Answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:  # Check for content in the current chunk
            Answer += chunk.choices[0].delta.content  # Append the content to the answer
    Answer = Answer.replace("</s>", "")  # Remove unwanted tokens from the response
    messages.append({"role": "assistant", "content": Answer})  # Add the AI's response to messages
    return Answer

# Function to search for a topic on YouTube
def YouTubeSearch(Topic):
    UrlSearch = f"https://www.youtube.com/results?search_query={Topic}"  # Construct the YouTube search URL
    webbrowser.open(UrlSearch)  # Open the URL in a web browser
    return True  # Indicate success

# YouTubeSearch("who is narendra modi")

# Function to play a video directly on YouTube
def PlayYoutube(query):
    playonyt(query)  # Use pywhatkit's function to play the video
    return True  # Indicate success

# PlayYoutube("machine learning")



# Function to open an application
def OpenApp(app):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)  # Attempt to open the app
        return True  # Indicate success
    except:
        return False  # Indicate failure

# OpenApp("setiings")

# Function to extract links from HTML content
def extract_links(html):
    if html is None:
        return []
    soup = BeautifulSoup(html, "html.parser")  # Parse the HTML content
    links = soup.find_all('a', {'jsname': 'UWckNb'})  # Find relevant links
    return [link.get('href') for link in links]  # Return the links

# Function to perform a Google search and retrieve HTML
def search_google(query, sess):
    url = f"https://www.google.com/search?q={query}"  # Construct the Google search URL
    headers = {"User-Agent": useragent}  # Use the predefined user-agent
    response = sess.get(url, headers=headers)  # Perform the GET request
    if response.status_code == 200:
        return response.text  # Return the HTML content
    else:
        print("Failed to retrieve search results.")  # Print an error message
        return None

# Function to close an application
def CloseApp(app):
    if "chrome" in app:
        pass  # Skip if the app is Chrome
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)  # Attempt to close the app
            return True  # Indicate success
        except:
            return False  # Indicate failure

# Function to execute system-level commands
def System(command):
    def mute():
        keyboard.press_and_release("volume mute")  # Simulate the mute key press

    def unmute():
        keyboard.press_and_release("volume mute")  # Simulate the unmute key press

    def volume_up():
        keyboard.press_and_release("volume up")  # Simulate the volume up key press

    def volume_down():
        keyboard.press_and_release("volume down")  # Simulate the volume down key press

    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
    return True

# Asynchronous function to translate and execute commands
async def TranslateAndExecute(commands: List[str]):
    funcs = []  # List to store asynchronous tasks
    for command in commands:
        if command.startswith("open"):
            if "open it" in command or "open file" in command:
                pass  # Ignore "open it" and "open file" commands
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open"))  # Schedule app opening
                funcs.append(fun)
        elif command.startswith("close"):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close"))  # Schedule app closing
            funcs.append(fun)
        elif command.startswith("play"):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play"))  # Schedule YouTube playback
            funcs.append(fun)
        elif command.startswith("content"):
            fun = asyncio.to_thread(Content, command.removeprefix("content"))  # Schedule content creation
            funcs.append(fun)
        elif command.startswith("google search"):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search"))  # Schedule Google search
            funcs.append(fun)
        elif command.startswith("youtube search"):
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search"))  # Schedule YouTube search
            funcs.append(fun)
        elif command.startswith("system"):
            fun = asyncio.to_thread(System, command.removeprefix("system"))  # Schedule system command
            funcs.append(fun)
        else:
            print(f"No Function Found for {command}")  # Print a message for unrecognized commands
    results = await asyncio.gather(*funcs)  # Execute all tasks concurrently
    for result in results:
        if isinstance(result, str):
            yield result

# Asynchronous function to automate commands
async def Automation(commands: List[str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True

