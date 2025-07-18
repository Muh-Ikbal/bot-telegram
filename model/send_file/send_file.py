from telegram import Update
import os
from telegram.ext import ContextTypes
from config import database
import requests
from dotenv import load_dotenv
import base64

load_dotenv()

api_url = os.getenv("API_URL")


async def handler_income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user = update.message.from_user
    user_name = user.name
    user_id = user.id
    if message.text:
        try:
            document = message.text
            
            payload = {
                "name" : user_name,
                "id" : user_id,
                "text": document
            }

            response = requests.post(
                f"{api_url}/api/cashflow/text",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                result = response.text
                await update.message.reply_text(result)
            else:
                await update.message.reply_text(f"Gagal memproses text: {response.text}")
            context.user_data.pop("mode", None)
        except Exception as e:
            await update.message.reply_text(f"terjadi kesalahan : {e}")

    elif message.photo:
        try:
            document = message.photo[-1]
            file = await context.bot.get_file(document.file_id)
            file_path = f"/tmp/{document.file_unique_id}"
            await file.download_to_drive(file_path)
            with open(file_path, "rb") as file:
                encoded_file = base64.b64encode(file.read()).decode("utf-8")
            payload = {
                "name" : user_name,
                "id" : user_id,
                "file_name": "gambar.jpg", 
                "file_data": encoded_file
                }

            response = requests.post(
                f"{api_url}/api/cashflow/image",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            if response.status_code == 200:
                result = response.text
                await update.message.reply_text(result)
            else:
                await update.message.reply_text(f"Gagal mengirim file: {response.text}")
        except Exception as e:
            await update.message.reply_text(f"terjadi kesalahan : {e}")

    elif message.document:
        if (
            message.document.mime_type
            == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ):
            try:
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
                    "name" : user_name,
                    "id" : user_id,
                    "file_name": "x.xlsx", 
                    "file_data": encoded_file
                    }

                # Kirim request POST
                response = requests.post(
                    f"{api_url}/api/ebitda_cost/file",
                    json=payload,
                    headers={"Content-Type": "application/json"},
                )
                if response.status_code == 200:
                    result = response.text
                    await update.message.reply_text(result)
                else:
                    await update.message.reply_text(f"Gagal mengirim file: {response.text}")
            except Exception as e:
                await update.message.reply_text(f"terjadi kesalahan : {e}")
        else:
            await message.reply_text("Tolong masukkan file exce (.xlsx)")

    else:
        await message.reply_text(
            "Mohon kirim data dalam bentuk teks, foto, atau file .xlsx."
        )
    context.user_data["command"] = ""


async def handler_outcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user = update.message.from_user
    user_name = user.name
    user_id = user.id
    if message.text:
        try:
            document = message.text

            payload = {
                "name" : user_name,
                "id" : user_id,
                "text": document
            }

            response = requests.post(
                f"{api_url}/api/cashflow/text",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                result = response.text
                await update.message.reply_text(result)
            else:
                await update.message.reply_text(f"Gagal memproses text: {response.text}")
            context.user_data.pop("mode", None)
        except Exception as e:
            await update.message.reply_text(f"terjadi kesalahan : {e}")

    elif message.photo:
        try:
            document = message.photo[-1]
            file = await context.bot.get_file(document.file_id)
            file_path = f"/tmp/{document.file_unique_id}"
            await file.download_to_drive(file_path)

            with open(file_path, "rb") as file:
                encoded_file = base64.b64encode(file.read()).decode("utf-8")
            payload = {
                "name": user_name,
                "id": user_id,
                "file_name": "gambar.jpg",
                "file_data": encoded_file,
            }

            response = requests.post(
                f"{api_url}/api/cashflow/image",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            if response.status_code == 200:
                result = response.text
                await update.message.reply_text(result)
            else:
                await update.message.reply_text(f"Gagal mengirim file: {response.text}")
        except Exception as e:
            await update.message.reply_text(f"terjadi kesalahan : {e}")

    elif message.document:
        if (
            message.document.mime_type
            == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ):
            try:
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
                    "name": user_name,
                    "id": user_id,
                    "file_name": "x.xlsx",
                    "file_data": encoded_file,
                }

                # Kirim request POST
                response = requests.post(
                    f"{api_url}/api/ebitda_cost/file",
                    json=payload,
                    headers={"Content-Type": "application/json"},
                )
                if response.status_code == 200:
                    result = response.text
                    await update.message.reply_text(result)
                else:
                    await update.message.reply_text(f"Gagal mengirim file: {response.text}")
            except Exception as e:
                await update.message.reply_text(f"terjadi kesalahan : {e}")
        else:
            await message.reply_text("Tolong masukkan file exce (.xlsx)")

    else:
        await message.reply_text(
            "Mohon kirim data dalam bentuk teks, foto, atau file .xlsx."
        )
    context.user_data["command"] = ""
