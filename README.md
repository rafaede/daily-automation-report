# Daily Automation Report Tool

Script Python yang otomatis bikin laporan harian, gabungan dari:
- Kurs USD ke IDR real-time (via public API)
- Data kota dari file CSV
- Insight AI pakai Google Gemini API (output JSON terstruktur: sentiment, insight, saran aksi)
- Notifikasi ringkasan ke Telegram

## Cara pakai
1. Install dependencies: `pip install -r requirements.txt`
2. Bikin file `.env` isi:
```
   GEMINI_API_KEY=api_key_kamu
   TELEGRAM_BOT_TOKEN=token_bot_kamu
   TELEGRAM_CHAT_ID=chat_id_kamu
```
3. Jalankan: `python laporan_harian.py`

## Output
Hasil ke-append ke `laporan.txt`: ada timestamp, kurs, sentiment, insight, saran aksi dari AI, dan ringkasan kota. Kalau panggilan AI gagal, ada retry otomatis lalu fallback ke teks default.

## Telegram Notification
Setelah laporan tersimpan, script ngirim satu pesan ke Telegram berisi kurs, sentiment, insight, dan saran aksi. Token bot didapat dari @BotFather. Kalau pengiriman gagal, script cuma nampilin pesan error singkat dan tidak menampilkan token.