from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt

# Load environment variables from the `.env` file.
env_vars = dotenv_values(".env")

# Get the input language setting from the environment variables.
InputLanguage = env_vars.get("InputLanguage", "en")

# Define the HTML code for the speech recognition interface.

HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

# Replace the language setting in the HTML code with the input language from the environment variables.
HtmlCode = HtmlCode.replace("{LANGUAGE}", InputLanguage)

# Write the modified HTML code to a file.
os.makedirs("Data", exist_ok=True)  # Ensure the directory exists
with open(r"Data\Voice.html", "w", encoding="utf-8") as f:
    f.write(HtmlCode)

# Get the current working directory.
current_dir = os.getcwd()

# Generate the file path for the HTML file.
Link = f"file:///{current_dir}/Data/Voice.html"

# Set Chrome options for the WebDriver.
chrome_options = Options()
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.6.142.86 Safari/537.36"
)
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")

# Initialize WebDriver.
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to perform speech recognition using the WebDriver.
def SpeechRecognition():
    # Open the HTML file in the browser.
    driver.get(Link)

    # Start speech recognition by clicking the start button.
    driver.find_element(By.ID, "start").click()

    while True:
        try:
            # Get the recognized text from the HTML output element.
            Text = driver.find_element(By.ID, "output").text
            if Text:
                # Stop recognition by clicking the stop button.
                driver.find_element(By.ID, "end").click()
                
                # If the input language is English, return the modified query.
                if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                    return QueryModifier(Text)
                else:
                    # If the input language is not English, translate the text and return it.
                    SetAssistantStatus("Translating...")
                    return QueryModifier(UniversalTranslator(Text))
        except Exception as e:
            pass

# Function to modify user query.
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()

    question_words = [
        "how", "what", "who", "where", "when", "why", "which", "whose", "whom",
        "can you", "what's", "where's", "how's"
    ]

    if any(word in new_query for word in question_words):
        if query_words:
            new_query = new_query + "?"
        else:
            new_query = new_query.capitalize()

    return new_query

# Function to translate text to English.
def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation

# Function to set assistant status.
def SetAssistantStatus(Status):
    temp_dir_path = os.path.join(current_dir, "frontend", "Files")
    os.makedirs(temp_dir_path, exist_ok=True)  # Ensure the directory exists
    with open(os.path.join(temp_dir_path, "Status.data"), "w", encoding="utf-8") as file:
        file.write(Status)

# Main execution block.
if __name__ == "__main__":
    while True:
        # Continuously perform speech recognition.
        Text = SpeechRecognition()
        print(Text)
