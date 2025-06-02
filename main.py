import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "7831503778:AAGllIL2ENH59cQW_O3K3EgliLpZoF_9rKE"

IPINFO_TOKEN = "8f88466dc20815"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Silakan masukkan IP Address atau nama domain yang ingin Anda cek lokasinya:")

async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    
    url = f"https://ipinfo.io/{user_input}?token={IPINFO_TOKEN}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()

        ip = data.get("ip", "-")
        city = data.get("city", "-")
        region = data.get("region", "-")
        country = data.get("country", "-")
        postal = data.get("postal", "-")
        loc = data.get("loc", "") 
        org = data.get("org", "-")

        if loc:
            lat, lon = loc.split(",")
            google_maps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
        else:
            google_maps_link = "-"

        message = (
            f"🌐 Info Lokasi untuk: `{ip}`\n\n"
            f"🏙️ Kota/Kabupaten: {city}\n"
            f"🌆 Provinsi: {region}\n"
            f"📮 Kode Pos: {postal}\n"
            f"🌎 Negara: {country}\n"
            f"📡 ISP: {org}\n"
            f"🧭 Latitude: {lat if loc else '-'}\n"
            f"🧭 Longitude: {lon if loc else '-'}\n\n"
            f"📍 [Lihat di Google Maps]({google_maps_link})"
        )

        await update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)

    else:
        await update.message.reply_text("❌ Gagal mendapatkan data lokasi. Periksa IP/Domain atau token API.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input))

    print("Bot sedang berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
