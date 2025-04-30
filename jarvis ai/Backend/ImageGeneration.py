import asyncio
from random import randint
from PIL import Image
import requests
import os
from time import sleep

# 🛠️ Backend se Frontend ke path set karna
frontend_files_dir = os.path.abspath("ImageGeneration.data")  # Backend se Frontend ka path
image_generation_file = r"D:\projects\jarvis ai\Frontend\Files\ImageGeneration.data"


data_folder = r"Data"

# 📁 Ensure folders exist
os.makedirs(frontend_files_dir, exist_ok=True)
os.makedirs(data_folder, exist_ok=True)

# 📝 File create karna agar exist nahi karti
if not os.path.exists(image_generation_file):
    with open(image_generation_file, "w") as f:
        f.write("False, False")  # Default values

# 🔑 Hugging Face API Key (Directly in code as requested)
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
HuggingFaceAPIKey = "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"

headers = {"Authorization": f"Bearer {HuggingFaceAPIKey}"}
print("✅ Hugging Face API Key Loaded.")

# 🖼️ Function to open generated images
def open_images(prompt):
    prompt = prompt.replace(" ", "_")
    files = [os.path.join(data_folder, f"{prompt}{i}.jpg") for i in range(1, 5)]

    for image_path in files:
        try:
            img = Image.open(image_path)
            print(f"🖼️ Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"⚠️ Unable to open {image_path}")

# 🔄 Async API request function
async def query(payload, retries=3):
    for attempt in range(retries):
        try:
            response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
            if response.status_code == 200:
                return response.content
            print(f"⚠️ Attempt {attempt+1} failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Error in API Request: {e}")
        await asyncio.sleep(2)  # Retry delay
    return None

# 🚀 Image generation function
async def generate_images(prompt: str):
    tasks = []
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality 4K, sharpness-maximum, Ultra High details, high resolution, seed {randint(0, 1000000)}",
        }
        tasks.append(asyncio.create_task(query(payload)))

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        if image_bytes:
            image_path = os.path.join(data_folder, f"{prompt.replace(' ', '_')}{i + 1}.jpg")
            with open(image_path, "wb") as f:
                f.write(image_bytes)
            print(f"✅ Image saved: {image_path}")

# 🔥 Generate and open images
def GenerateImages(prompt: str):
    print(f"🚀 Generating images for prompt: '{prompt}'")
    asyncio.run(generate_images(prompt))
    open_images(prompt)

# 🔄 File monitoring loop
def monitor_file():
    max_retries = 30  # Max 30 attempts (~30 sec timeout)
    retry_count = 0

    while retry_count < max_retries:
        try:
            with open(image_generation_file, "r") as f:
                data = f.read().strip()
                print(f"📂 RAW File Data: '{data}'")  # ✅ Debugging log

            if "," in data:
                prompt, status = data.split(",", 1)
                prompt, status = prompt.strip(), status.strip().lower()

                print(f"📝 Parsed Prompt: '{prompt}', Status: '{status}'")  # ✅ Debugging log

                if status == "true":
                    print("🖼️ Generating Images...")
                    GenerateImages(prompt)

                    with open(image_generation_file, "w") as f:
                        f.write("False, False")

                    print("✅ Image generation complete. Exiting loop.")
                    break

            retry_count += 1
            sleep(1)

        except Exception as e:
            print(f"⚠️ Error: {e}")

    print("🛑 Exiting loop, timeout reached.")

# 🔥 Run the file monitor
monitor_file()
