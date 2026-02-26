# 🔥 Cloudflare WARP Config Generator

This project automatically downloads and updates Cloudflare WARP configuration files for different protocols and countries. It runs daily via GitHub Actions and pushes the updated configs to this repository and Telegram.

# 🔥 Important Usage & Security Notice

- Public configs in this repository are intended **only for normal usage** such as browsing websites and social media.
- Due to **high public usage and shared access**, these configs may become unstable, rate-limited, or stop working at any time.
- For **sensitive, private, or critical activities**, you MUST:
  - Fork this repository into your own **private GitHub repository**
  - Run the generator using your **own GitHub Actions**
  - Download configs **directly from your private repository**

Personal configs generated from your private repository have a higher connection success rate and stability compared to public shared configs.

---

# 🔥 Private Setup Guide (Step-by-Step)

## 🔥 Fork the Repository

1. Click **Fork** (top-right corner)  
2. Set repository visibility to **Private**  
3. Create the fork  

---


## 🔥 Run the GitHub Workflow

1. Go to the **Actions** tab  
2. Select the **Cloudflare WARP Auto-Update** workflow  
3. Click **Run workflow**  
4. Start execution  

The workflow will:
- Visit the WARP generator website
- Download AmneziaWG configs (3 per country)
- Download WireSock configs (1 per country)
- Package them into separate ZIP files
- Commit the ZIP files to your repository

---

## 🔥 Retrieve Your Configs

After successful execution:

- `WG-Tunnel.zip` and `WireSock.zip` will be generated
- They will be:
  - Committed directly to your private repository

Download the ZIP file and import the configurations into your preferred client:

- **Android**: Import `.conf` files into WG Tunnel app
- **Windows**: Import into WireSock client

---


## 🔥 Downloads

The generator creates two separate zip files:

| File | Protocol | Platform | Description |
|------|--|----------|-------------|
| [WG-Tunnel.zip](https://github.com/Delta-Kronecker/Cloudflare-Warp/raw/refs/heads/main/WG_Tunnel.zip) | WG Tunnel | Android | 3 configuration variants per country |
| [WireSock.zip](https://github.com/Delta-Kronecker/Cloudflare-Warp/raw/refs/heads/main/WireSock.zip) | WireSock | Windows | 1 configuration per country |

## 🔥 Supported Countries

- Standard (Default)
- Lithuania
- Germany 1
- Netherlands 1
- Germany 2
- Netherlands 2
- Finland

## 🔥 How to Use

### Android (WG Tunnel)

1. Download WG Tunnel from Google Play Store
2. Download the latest `WG-Tunnel.zip` from this repository
3. Open WG Tunnel app
5. Tap on " + "
6. Select the add from file or zip
7. Connect and enjoy!

### Windows (WireSock)

1. Download [WireSock](https://www.wiresock.net/) from the official website
2. Download the latest `WireSock.zip` from this repository
3. Extract the zip file
4. Open WireSock client
5. Copy the file to "\AppData\Local\WireSock Foundation\WireSock Secure Connect\Profiles"
6. Connect to the VPN
7. For using new configuration, delete the old file from folder and copy the new one

## 🔥 Telegram Channel

All configuration files are automatically sent to our Telegram channel. Join to get instant updates:

[**Join Telegram Channel**](https://t.me/DeltaKroneckerGithub) 



## ⚠️ Disclaimer

These configuration files are for educational and personal use only. Users are responsible for complying with their local laws and regulations regarding VPN usage.

## 🔥 Keep This Project Going!

If you're finding this useful, please show your support:

⭐ **Star the repository on GitHub**

⭐ **Star our [Telegram posts](https://t.me/DeltaKroneckerGithub)** 

Your stars fuel our motivation to keep improving!
