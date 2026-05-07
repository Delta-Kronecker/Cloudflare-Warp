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

# အာရှနိုင်ငံများစာရင်းသို့ ပြောင်းလဲခြင်း
COUNTRIES = [
    "Standard",
    "Singapore",
    "Japan",
    "Hong Kong",
    "South Korea",
    "Thailand"
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
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)

    def teardown(self):
        if self.driver:
            self.driver.quit()

    def human_pause(self, min_sec=2, max_sec=4):
        time.sleep(random.uniform(min_sec, max_sec))

    def patch_configs_for_port_500(self):
        """Download ဆွဲထားတဲ့ ဖိုင်တွေကို Port 500 ဖြစ်အောင် အတင်းလိုက်ပြင်ပေးမည့်အပိုင်း"""
        for filename in os.listdir(TEMP_DIR):
            if filename.endswith(".conf"):
                filepath = os.path.join(TEMP_DIR, filename)
                with open(filepath, 'r') as f:
                    content = f.read()
                
                # Endpoint ကို engage.cloudflareclient.com:500 သို့ အစားထိုးခြင်း
                import re
                new_content = re.sub(r'Endpoint = .*', 'Endpoint = engage.cloudflareclient.com:500', content)
                
                with open(filepath, 'w') as f:
                    f.write(new_content)
        print("All configs patched to engage.cloudflareclient.com:500")

    def create_zip(self, zip_name):
        # အရင်ဆုံး ဖိုင်တွေကို Port 500 ပြင်မယ်
        self.patch_configs_for_port_500()
        
        files = [f for f in os.listdir(TEMP_DIR) if os.path.isfile(os.path.join(TEMP_DIR, f))]
        if not files:
            return None
        
        zip_path = os.path.join(os.getcwd(), zip_name)
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for f in files:
                zf.write(os.path.join(TEMP_DIR, f), arcname=f)
        return zip_path

    def send_to_telegram(self, file_path, caption):
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID or not file_path:
            return
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
            with open(file_path, 'rb') as f:
                requests.post(url, data={'chat_id': TELEGRAM_CHAT_ID, 'caption': caption, 'parse_mode': 'Markdown'}, files={'document': f})
        except Exception as e:
            print(f"Telegram failed: {e}")

    def run(self):
        try:
            self.setup()
            self.driver.get("https://warp-generator.github.io/warp/")
            self.human_pause(5, 7)

            # Phase 1: WG Tunnel
            print("Processing WG Tunnel Phase...")
            for idx, country in enumerate(COUNTRIES):
                # Website ပေါ်မှာ နိုင်ငံရွေးတဲ့အပိုင်း (ရရင်ရွေး၊ မရရင် Standard နဲ့သွားမယ်)
                try:
                    settings_btn = self.driver.find_element(By.CSS_SELECTOR, "svg.settings-btn")
                    settings_btn.click()
                    self.human_pause(2, 3)
                    country_opt = self.driver.find_element(By.XPATH, f"//div[contains(text(), '{country}')]")
                    country_opt.click()
                    self.driver.find_element(By.CSS_SELECTOR, "span.close").click()
                except:
                    pass

                for btn_id in ["generateButton2", "generateButton3"]:
                    try:
                        self.driver.find_element(By.ID, btn_id).click()
                        self.human_pause(3, 5)
                    except: pass

            wg_zip = self.create_zip("WG-Tunnel.zip")

            # Phase 2: WireSock
            # အချိန်ကုန်သက်သာစေရန်နှင့် သေချာစေရန် WG_Tunnel ထဲကဖိုင်တွေကိုပဲ WireSock နာမည်နဲ့ သိမ်းပေးလိုက်ပါမယ်
            if wg_zip:
                wiresock_zip = os.path.join(os.getcwd(), "WireSock.zip")
                shutil.copy(wg_zip, wiresock_zip)
                
                print("Sending to Telegram...")
                self.send_to_telegram(wg_zip, "✅ **WG Tunnel (Asia + Port 500)**")
                self.send_to_telegram(wiresock_zip, "✅ **WireSock (Asia + Port 500)**")
            
            print("Done!")
        finally:
            self.teardown()

if __name__ == "__main__":
    WarpGeneratorDownloader().run()
