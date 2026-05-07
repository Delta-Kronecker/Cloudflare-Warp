import os, time, random, zipfile, shutil, requests, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# User Variables
S1, S2, Jc, Jmin, Jmax = 0, 0, 4, 40, 70
H1, H2, H3, H4, I1 = 1, 2, 3, 4, 0
COUNTRIES = ["Standard", "Singapore", "Japan", "Hong Kong", "Thailand", "South Korea"]
TEMP_DIR = os.path.join(os.getcwd(), "temp_downloads")
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

class WarpGenerator:
    def __init__(self):
        if os.path.exists(TEMP_DIR): shutil.rmtree(TEMP_DIR)
        os.makedirs(TEMP_DIR)
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("prefs", {"download.default_directory": TEMP_DIR, "profile.default_content_setting_values.automatic_downloads": 1})
        self.driver = webdriver.Chrome(options=options)

    def change_country(self, name):
        try:
            wait = WebDriverWait(self.driver, 10)
            btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.settings-btn")))
            btn.click()
            time.sleep(2)
            opt = self.driver.find_element(By.XPATH, f"//div[contains(text(), '{name}')]")
            opt.click()
            self.driver.find_element(By.CSS_SELECTOR, "span.close").click()
            time.sleep(2)
        except: pass

    def patch_configs(self):
        for f in os.listdir(TEMP_DIR):
            if f.endswith(".conf"):
                p = os.path.join(TEMP_DIR, f)
                with open(p, 'r', encoding='utf-8') as file:
                    data = file.read()
                data = re.sub(r'Endpoint = .*', 'Endpoint = engage.cloudflareclient.com:500', data)
                data = "# Port 500 Asia Server\n" + data
                with open(p, 'w', encoding='utf-8') as file:
                    file.write(data)

    def run(self):
        try:
            self.driver.get("https://warp-generator.github.io/warp/")
            time.sleep(5)
            for c in COUNTRIES:
                self.change_country(c)
                for i in range(H2, Jc + 1):
                    try:
                        self.driver.find_element(By.ID, f"generateButton{i}").click()
                        time.sleep(random.uniform(Jmin/10, Jmax/10))
                    except: pass
            self.patch_configs()
            z_path = os.path.join(os.getcwd(), "WG-Tunnel.zip")
            with zipfile.ZipFile(z_path, 'w', zipfile.ZIP_DEFLATED) as z:
                for f in os.listdir(TEMP_DIR):
                    z.write(os.path.join(TEMP_DIR, f), arcname=f)
            shutil.copy(z_path, "WireSock.zip")
            self.send(z_path, "✅ WG Tunnel (Asia 500)")
            self.send("WireSock.zip", "✅ WireSock (Asia 500)")
        finally:
            self.driver.quit()

    def send(self, p, cap):
        if TOKEN and CHAT_ID:
            with open(p, 'rb') as f:
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendDocument", data={'chat_id': CHAT_ID, 'caption': cap}, files={'document': f})

if __name__ == "__main__":
    WarpGenerator().run()
                    except: pass

            # Port 500 သို့ ပြင်ဆင်ခြင်း
            self.patch_configs_to_port_500()

            # Zip ဖိုင်များ ဖန်တီးခြင်း
            wg_zip = self.create_zip("WG-Tunnel.zip")
            if wg_zip:
                # WireSock အတွက် တိုက်ရိုက်ပွားယူခြင်း
                wiresock_zip = os.path.join(os.getcwd(), "WireSock.zip")
                shutil.copy(wg_zip, wiresock_zip)

                # Telegram သို့ ပို့ဆောင်ခြင်း
                self.send_to_telegram(wg_zip, "✅ **WG Tunnel (Asia + Port 500)**")
                self.send_to_telegram(wiresock_zip, "✅ **WireSock (Asia + Port 500)**")
            
            print("Successfully Completed.")
        finally:
            if self.driver: self.driver.quit()

    def send_to_telegram(self, file_path, caption):
        if not (TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID): return
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
        with open(file_path, 'rb') as f:
            requests.post(url, data={'chat_id': TELEGRAM_CHAT_ID, 'caption': caption, 'parse_mode': 'Markdown'}, files={'document': f})

if __name__ == "__main__":
    WarpGeneratorDownloader().run()
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
