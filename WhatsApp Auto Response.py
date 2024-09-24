import time
import json
import random
import logging
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration: Update these paths as necessary
CHROME_DRIVER_PATH = 'path/to/chromedriver'
CONFIG_FILE_PATH = 'config.json'  # Path to JSON file containing keywords and responses

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('whatsapp_bot.log'),
        logging.StreamHandler()
    ]
)

class WhatsAppBot:
    def __init__(self, chrome_driver_path, config_file):
        self.driver = self.init_driver(chrome_driver_path)
        self.keywords_responses = self.load_config(config_file)
        self.is_running = True  # Used to pause or resume the bot
        self.polling_interval = 10  # Default polling interval in seconds

    def load_config(self, file_path):
        """Load keyword-response configuration from a JSON file."""
        with open(file_path, 'r') as file:
            config = json.load(file)
        return config

    def init_driver(self, chrome_driver_path):
        """Initialize the WebDriver with optional headless mode."""
        service = Service(chrome_driver_path)
        options = webdriver.ChromeOptions()
        options.add_argument('--user-data-dir=./User_Data')  # Persist session to avoid re-login
        # Uncomment below line for headless mode (no browser UI)
        # options.add_argument('--headless')
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def wait_for_login(self):
        """Wait for the user to scan the QR code and log in to WhatsApp Web."""
        self.driver.get('https://web.whatsapp.com')
        logging.info("Waiting for user to log in via QR code...")
        WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.ID, 'pane-side'))
        )
        logging.info("Login successful!")

    def select_random_response(self, responses):
        """Select a random response from the list of possible responses."""
        return random.choice(responses)

    def pause_bot(self):
        """Pause the bot."""
        logging.info("Bot paused.")
        self.is_running = False

    def resume_bot(self):
        """Resume the bot."""
        logging.info("Bot resumed.")
        self.is_running = True

    def respond_to_messages(self):
        """Monitor WhatsApp messages and respond to specific keywords."""
        while self.is_running:
            try:
                unread_msgs = WebDriverWait(self.driver, self.polling_interval).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, '_1pJ9J'))
                )

                for msg in unread_msgs:
                    msg.click()
                    time.sleep(random.uniform(1, 3))  # Random delay to mimic human behavior

                    msg_text_elements = self.driver.find_elements(By.CSS_SELECTOR, 'span.selectable-text span')
                    if msg_text_elements:
                        last_msg_text = msg_text_elements[-1].text.lower()
                        logging.info(f"Received message: {last_msg_text}")

                        for keyword, responses in self.keywords_responses.items():
                            if keyword.lower() in last_msg_text:
                                response = self.select_random_response(responses)
                                logging.info(f"Responding with: {response}")

                                input_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
                                input_box.send_keys(response + Keys.ENTER)
                                time.sleep(random.uniform(1, 2))  # Random delay to prevent spamming
                                break

                time.sleep(random.uniform(5, 10))  # Random delay to mimic human behavior

            except Exception as e:
                logging.error(f"An error occurred while processing messages: {e}")
                time.sleep(5)

    def start(self):
        """Start the bot with login and message handling."""
        try:
            self.wait_for_login()

            # Create a separate thread for responding to messages
            message_thread = threading.Thread(target=self.respond_to_messages)
            message_thread.start()

        except Exception as e:
            logging.error(f"An error occurred in the main function: {e}")
        finally:
            self.driver.quit()
            logging.info("Driver closed.")

    def stop(self):
        """Stop the bot gracefully."""
        logging.info("Stopping bot...")
        self.is_running = False

    def reconnect(self):
        """Reconnect the bot in case of a disconnection."""
        logging.info("Reconnecting...")
        self.driver.quit()
        self.driver = self.init_driver(CHROME_DRIVER_PATH)
        self.wait_for_login()

    def send_media(self, image_path):
        """Send media file (image, gif, etc.) to a WhatsApp contact."""
        try:
            attach_btn = self.driver.find_element(By.CSS_SELECTOR, "span[data-icon='clip']")
            attach_btn.click()
            time.sleep(1)

            image_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            image_input.send_keys(image_path)
            time.sleep(2)  # Wait for the image to load in the chat

            send_btn = self.driver.find_element(By.CSS_SELECTOR, "span[data-icon='send']")
            send_btn.click()

            logging.info(f"Sent media: {image_path}")
        except Exception as e:
            logging.error(f"Failed to send media: {e}")

def main():
    """Main function to run the WhatsApp auto-responder bot."""
    bot = WhatsAppBot(CHROME_DRIVER_PATH, CONFIG_FILE_PATH)

    try:
        bot.start()

        # Monitor user input to control the bot (e.g., pausing/resuming/stopping)
        while True:
            command = input("Enter 'pause', 'resume', or 'stop': ").strip().lower()
            if command == 'pause':
                bot.pause_bot()
            elif command == 'resume':
                bot.resume_bot()
            elif command == 'stop':
                bot.stop()
                break

    except Exception as e:
        logging.error(f"An error occurred in the main function: {e}")
    finally:
        bot.driver.quit()
        logging.info("Driver closed.")

if __name__ == "__main__":
    main()