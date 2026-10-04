import requests
import csv
from datetime import datetime
from dotenv import load_dotenv
from google import genai
import os
import time
import json

def kirim_telegram(pesan):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id":chat_id,
            "text":pesan}

    
    try:
        response = requests.post(url,data=data,timeout=10)
        print(response.status_code)
    except Exception: 
        print("gagal kirim telegram")

def main():
    try:
        #request api
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        idr_usd = response.json()['rates']['IDR']
        
        #buka csv
        kota = {}
        with open('data.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for line in reader:
                if line[2] in kota:
                    kota[line[2]] += 1
                else:
                    kota[line[2]] = 1
            
        with open('laporan.txt', 'a') as f:
            f.write(f"{datetime.now()}\n")
            f.write(f"USD to IDR: [{idr_usd}]\n")
            load_dotenv()
            data =  {"sentiment":"-",
                        "insight":"AI insight tidak tersedia saat ini",
                        "saran_aksi":"-"}
            api_key = os.getenv("GEMINI_API_KEY")
            for percobaan in range(3):
                try :
                    
                    client = genai.Client(api_key=api_key)
                    response = client.models.generate_content(
                        model="gemini-3.5-flash",
                        contents=f"""
                        Kurs USD ke IDR saat ini adalah Rp{idr_usd}.Berikan 1 kalimat insight sederhana tentang kondisi kurs tersebut dan apa artinya bagi orang yang ingin menukar uang.
                        Jawab HANYA dengan JSON, tanpa teks lain, dengan format:
                        {{ "sentiment" :" salah satu dari (positif/negatif/netral)", "insight":"1 kalimat sederhana tentang kondisi kurs", "saran_aksi":  "1 kalimat saran buat orang yang mau tuker uang"}}
                        """
                    )
                    data = json.loads(response.text)
                    print(data["sentiment"])
                    break
                except Exception as e:
                    time.sleep(5)
                    print(f"Percobaan gagal: {e}")
            f.write(f"{data["sentiment"]}\n")
            f.write(f"{data["insight"]}\n")
            f.write(f"{data["saran_aksi"]}\n")
            for nama_kota, jumlah in kota.items():
                f.write(f"{nama_kota} : {jumlah}\n")
            f.write(f"---\n")
            
        kirim_telegram(f"USD to IDR: [{idr_usd}]\nSentiment : {data["sentiment"]}\nInsight : {data["insight"]}\nSaran Aksi : {data["saran_aksi"]}")    
 
        
    except Exception as e:
        print("Error: ",e)
    
    
if __name__ == "__main__":
    main()