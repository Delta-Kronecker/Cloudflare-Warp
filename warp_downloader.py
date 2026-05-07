import os, time, random, zipfile, shutil, requests, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Constants (မူရင်း Variable များအတိုင်း ပြန်ထားသည်)
S1, S2 = 0, 0
Jc = 4
Jmin, Jmax = 40, 70
H1, H2, H3, H4 = 1, 2, 3, 4
I1 = 0

# နိုင်ငံများကို အာရှနိုင်ငံများဖြင့် အစားထိုးသည်
COUNTRIES = ["Standard", "Singapore", "Japan", "Hong Kong", "Thailand", "South Korea"]

TEMP_DIR = os.path.join(os.getcwd(), "temp_downloads")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

class WarpGeneratorDownloader:
    def __init__(self):
        self.driver = None
        if os.path.exists(TEMP_DIR): shutil.rmtree(TEMP_DIR)
        os.makedirs(TEMP_DIR)

    def setup(self):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        prefs = {
            "download.default_directory": TEMP_DIR,
            "download.prompt_for_download": False,
            "profile.default_content_setting_values.automatic_downloads": 1
        }
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=options)

    def change_country(self, country_name):
        try:
            wait = WebDriverWait(self.driver, 10)
            settings_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.settings-btn")))
            settings_btn.click()
            time.sleep(2)
            # နိုင်ငံကို ရှာဖွေနှိပ်ခြင်း
            country_opt = self.driver.find_element(By.XPATH, f"//div[contains(text(), '{country_name}')]")
            country_opt.click()
            self.driver.find_element(By.CSS_SELECTOR, "span.close").click()
            time.sleep(2)
        except: pass

    def patch_configs(self):
        """သိမ်းခါနီးတွင် Port 500 အဖြစ် အတင်းလိုက်ပြင်ဆင်ခြင်း"""
        for filename in os.listdir(TEMP_DIR):
            if filename.endswith(".conf"):
                filepath = os.path.join(TEMP_DIR, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Port ပြောင်းလဲခြင်း
                content = re.sub(r'Endpoint = .*', 'Endpoint = engage.cloudflareclient.com:500', content)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

    def run(self):
        try:
            self.setup()
            self.driver.get("https://warp-generator.github.io/warp/")
            time.sleep(5)

            for country in COUNTRIES:
                self.change_country(country)
                # မူရင်းခလုတ်များ (2 မှ 4 အထိ) ကို နှိပ်ခြင်း
                for i in range(H2, Jc + 1):
                    try:
                        self.driver.find_element(By.ID, f"generateButton{i}").click()
                        time.sleep(random.uniform(Jmin/10, Jmax/10))
                    except: pass

            # အရေးကြီးဆုံးအပိုင်း- Port 500 ပြင်မည်
            self.patch_configs()

            # Zip လုပ်ပြီး သိမ်းဆည်းခြင်း
            wg_zip = os.path.join(os.getcwd(), "WG-Tunnel.zip")
            files = [f for f in os.listdir(TEMP_DIR) if f.endswith(".conf")]
            if files:
                with zipfile.ZipFile(wg_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for f in files: zf.write(os.path.join(TEMP_DIR, f), arcname=f)
                
                # WireSock အတွက် copy ကူးသည်
                shutil.copy(wg_zip, os.path.join(os.getcwd(), "WireSock.zip"))
                
                # Telegram သို့ ပို့သည်
                self.send_to_telegram(wg_zip, "✅ WG Tunnel (Asia 500)")
                self.send_to_telegram("WireSock.zip", "✅ WireSock (Asia 500)")
        finally:
            if self.driver: self.driver.quit()

    def send_to_telegram(self, p, cap):
        if not (TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID): return
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
        with open(p, 'rb') as f:
            requests.post(url, data={'chat_id': TELEGRAM_CHAT_ID, 'caption': cap}, files={'document': f})

if __name__ == "__main__":
    WarpGeneratorDownloader().run()
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
