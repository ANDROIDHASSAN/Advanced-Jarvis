import pygame  # For handling audio playback
import random  # For generating random choices
import asyncio  # For asynchronous operations
import edge_tts  # For text-to-speech functionality
import os  # For file path handling
from dotenv import dotenv_values  # For reading environment variables from a .env file

# Load environment variables
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice", "en-US-GuyNeural")  # Default voice

# Define file path
file_path = r"Data/speech.mp3"

# Asynchronous function to convert text to an audio file
async def TextToAudioFile(text) -> None:
    if os.path.exists(file_path):
        try:
            os.remove(file_path)  # Remove file if it already exists
        except Exception as e:
            print(f"Error deleting old file: {e}")

    # Generate speech
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch="+5Hz", rate="+13%")
    await communicate.save(r'Data\speech.mp3')

# Function to play TTS using pygame
def TTS(Text, func=lambda _: True):
    try:
        asyncio.run(TextToAudioFile(Text))  # Convert text to speech
        pygame.mixer.init()  # Initialize pygame mixer
        pygame.mixer.music.load(file_path)  # Load audio file
        pygame.mixer.music.play()  # Play audio

        # Wait until the audio is done playing
        while pygame.mixer.music.get_busy():
            if not func(True):  # Ensure func handles a boolean argument
                break
            pygame.time.Clock().tick(10)  # Limit the loop to 10 ticks per second

        return True  # Return success

    except Exception as e:
        print(f"Error in TTS: {e}")
        return False

    finally:
        try:
            func(False)  # Signal end of TTS
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            
            # Ensure the file is properly closed before deleting
            if os.path.exists(file_path):
                pygame.time.wait(500)  # Give it some time to release the file
                os.remove(file_path)  # Now delete the file safely
        except Exception as e:
            print(f"Error in cleanup: {e}")

# Function to handle long text-to-speech conversion
def TextToSpeech(Text, func=lambda _: True):
    sentences = Text.split(".")  # Split text into sentences
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]

    if len(sentences) > 4 and len(Text) >= 250:
        TTS(".".join(sentences[:2]) + ". " + random.choice(responses), func)
    else:
        TTS(Text, func)

# Main execution loop
if __name__ == "__main__":
    while True:
        try:
            text = input("Enter the text (or type 'exit' to quit): ")
            if text.lower() == "exit":
                break
            TextToSpeech(text)
        except KeyboardInterrupt:
            print("\nExiting program.")
            break
