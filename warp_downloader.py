import os
import time
import random
import zipfile
import shutil
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Constants
TEMP_DIR = os.path.join(os.getcwd(), "temp_downloads")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

COUNTRIES = [
    "Standard",
    "🇱🇹 Литва",
    "🇩🇪 Германия 1",
    "🇳🇱 Нидерланды 1",
    "🇩🇪 Германия 2",
    "🇳🇱 Нидерланды 2",
    "🇫🇮 Финляндия"
]

class WarpGeneratorDownloader:
    def __init__(self):
        self.driver = None
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)
        os.makedirs(TEMP_DIR)

    def setup(self):
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        prefs = {
            "download.default_directory": TEMP_DIR,
            "download.prompt_for_download": False,
            "plugins.always_open_pdf_externally": True,
            "profile.default_content_setting_values.automatic_downloads": 1
        }
        options.add_experimental_option("prefs", prefs)
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        options.add_argument("--start-maximized")
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def teardown(self):
        if self.driver:
            self.driver.quit()
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)

    def human_pause(self, min_sec=1, max_sec=3):
        time.sleep(random.uniform(min_sec, max_sec))

    def change_country(self, country_name):
        try:
            settings_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.settings-btn"))
            )
            self.human_pause(1, 2)
            settings_btn.click()
            self.human_pause(2, 3)

            country_option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{country_name}')]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", country_option)
            self.human_pause(1, 2)
            country_option.click()
            self.human_pause(2, 3)

            close_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "span.close"))
            )
            close_btn.click()
            self.human_pause(2, 3)
            return True
        except Exception as e:
            print(f"Error changing to {country_name}: {e}")
            try:
                close_btn = self.driver.find_element(By.CSS_SELECTOR, "span.close")
                close_btn.click()
            except:
                pass
            return False

    def create_zip(self, zip_name):
        files = [f for f in os.listdir(TEMP_DIR) if os.path.isfile(os.path.join(TEMP_DIR, f))]
        if not files:
            print(f"No files for {zip_name}")
            return None
        zip_path = os.path.join(os.getcwd(), zip_name)
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for f in files:
                zf.write(os.path.join(TEMP_DIR, f), arcname=f)
        print(f"Created {zip_name} with {len(files)} files")
        return zip_path

    def send_to_telegram(self, file_path, caption):
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            print("Telegram credentials missing, skipping upload")
            return
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
            with open(file_path, 'rb') as f:
                response = requests.post(url,
                    data={'chat_id': TELEGRAM_CHAT_ID, 'caption': caption, 'parse_mode': 'Markdown'},
                    files={'document': f}
                )
            if response.status_code == 200:
                print(f"Sent {os.path.basename(file_path)} to Telegram")
            else:
                print(f"Telegram error: {response.text}")
        except Exception as e:
            print(f"Telegram send failed: {e}")

    def run(self):
        try:
            self.setup()
            print("Loading website...")
            self.driver.get("https://warp-generator.github.io/warp/")
            self.human_pause(5, 7)

            # Phase 1: AmneziaWG (3 per country)
            print("\nPhase 1: AmneziaWG")
            for idx, country in enumerate(COUNTRIES):
                print(f"\nProcessing {country}")
                if idx > 0 and not self.change_country(country):
                    continue
                for btn_id in ["generateButton2", "generateButton3", "generateButton4"]:
                    try:
                        btn = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.ID, btn_id))
                        )
                        self.human_pause(1, 2)
                        btn.click()
                        self.human_pause(4, 6)
                    except Exception as e:
                        print(f"Error clicking {btn_id}: {e}")
            
            amnezia_zip = self.create_zip("AmneziaWG.zip")
            
            # Clear temp directory for next phase
            for f in os.listdir(TEMP_DIR):
                os.remove(os.path.join(TEMP_DIR, f))

            print("\nReturn to Standard")
            self.change_country("Standard")

            # Phase 2: WireSock (1 per country)
            print("\nPhase 2: WireSock")
            for idx, country in enumerate(COUNTRIES):
                print(f"\nProcessing {country}")
                if idx > 0 and not self.change_country(country):
                    continue
                try:
                    btn = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "generateButton10"))
                    )
                    self.human_pause(1, 2)
                    btn.click()
                    self.human_pause(4, 6)
                except Exception as e:
                    print(f"Error downloading WireSock: {e}")
            
            wiresock_zip = self.create_zip("WireSock.zip")

            # Send both files to Telegram
            print("\nSending files to Telegram...")
            
            amnezia_caption = (
                "**AmneziaWG Configs**\n\n"
                f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}\n"
                f"Countries: {len(COUNTRIES)}\n"
                "3 variants per country"
            )
            self.send_to_telegram(amnezia_zip, amnezia_caption)

            wiresock_caption = (
                "**WireSock Configs**\n\n"
                f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}\n"
                f"Countries: {len(COUNTRIES)}\n"
                "1 config per country"
            )
            self.send_to_telegram(wiresock_zip, wiresock_caption)

            print("\nAll done.")
        finally:
            self.teardown()

if __name__ == "__main__":
    downloader = WarpGeneratorDownloader()
    downloader.run()
