# Daily Automation Report Tool

Script Python yang otomatis bikin laporan harian, gabungan dari:
- Kurs USD ke IDR real-time (via public API)
- Data kota dari file CSV
- Insight AI pakai Google Gemini API

## Cara pakai
1. Install dependencies: `pip install -r requirements.txt`
2. Bikin file `.env` isi: `GEMINI_API_KEY=api_key_kamu`
3. Jalankan: `python laporan_harian.py`

## Output
Hasil ke-append ke `laporan.txt` — ada timestamp, kurs, ringkasan kota, dan insight dari AI (dengan retry + fallback otomatis kalau panggilan AI-nya gagal).