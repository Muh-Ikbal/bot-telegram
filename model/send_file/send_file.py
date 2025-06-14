from telegram import Update
import os
from telegram.ext import ContextTypes
from config import database
import requests
from dotenv import load_dotenv
import base64

load_dotenv()

api_url = os.getenv("API_URL")


async def handler_xlsx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        mode = context.user_data.get("mode")
        if not mode:
            await update.message.reply_text(
                "Kirim command terlebih dahulu seperti: \n/input_file_cost"
            )
            return
        document = update.message.document
        if not document.file_name.endswith(".xlsx"):
            await update.message.reply_text("Silahkan kirim file excel (.xlsx)")
            return
        file = await context.bot.get_file(document.file_id)
        file_path = f"/tmp/{document.file_name}"
        await file.download_to_drive(file_path)

        # Baca file dan encode ke base64
        with open(file_path, "rb") as file:
            encoded_file = base64.b64encode(file.read()).decode("utf-8")

        # Siapkan payload JSON
        payload = {
            "file_name": "x.xlsx",
            "file_data": encoded_file
        }

        # Kirim request POST
        response = requests.post(
            f"{api_url}/api/ebitda_cost/file",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            result = response.text
            await update.message.reply_text(result)
        else:
            await update.message.reply_text(f"Gagal mengirim file: {response.text}")
        context.user_data.pop("mode", None)
    except Exception as e:
        await update.message.reply_text(f"terjadi kesalahan : {e}")
