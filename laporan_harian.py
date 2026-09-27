import requests
import csv
from datetime import datetime
from dotenv import load_dotenv
from google import genai
import os
import time
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
            insight =  "AI insight tidak tersedia saat ini"
            api_key = os.getenv("GEMINI_API_KEY")
            for percobaan in range(3):
                try :
                    
                    client = genai.Client(api_key=api_key)
                    response = client.models.generate_content(
                        model="gemini-3.5-flash",
                        contents=f"Kurs USD ke IDR saat ini adalah Rp{idr_usd}.Berikan 1 kalimat insight sederhana tentang kondisi kurs tersebut dan apa artinya bagi orang yang ingin menukar uang."
                    )
                    insight = response.text
                    break
                except Exception as e:
                    time.sleep(5)
                    print(f"Percobaan gagal: {e}")
            f.write(f"{insight}\n")
            for nama_kota, jumlah in kota.items():
                f.write(f"{nama_kota} : {jumlah}\n")
            f.write(f"---\n")
                
    except Exception as e:
        print("Error: ",e)
    
    
if __name__ == "__main__":
    main()