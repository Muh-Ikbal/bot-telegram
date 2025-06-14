import pandas as pd
from telegram import Update
import os
from dotenv import load_dotenv
from telegram.ext import ContextTypes
from config import database


async def handler_xlsx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("testing jalan")
    try:
        mode = context.user_data.get("mode")
        if not mode:
            await update.message.reply_text(
                "Kirim command terlebih dahulu seperti: \n/tambah_barang, atau \n/tambah_keuangan"
            )
            return
        document = update.message.document
        if not document.file_name.endswith(".xlsx"):
            await update.message.reply_text("Silahkan kirim file excel (.xlsx) saja")
            return
        file = await context.bot.get_file(document.file_id)
        file_path = f"/tmp/{document.file_name}"
        await file.download_to_drive(file_path)

        df = pd.read_excel(file_path)

        if mode == "barang":
            required_columns = {
                "nama_product",
                "stock_toko",
                "stock_gudang",
                "stock_kampas",
            }
            if not required_columns.issubset(df.columns):
                await update.message.reply_text(
                    f"Format kolom untuk tambah data barang salah. Kolom yang dibutuhkan : {', '.join(required_columns)}"
                )
                return
            records = df.to_dict(orient="records")
            # database.supabase.table("stock_product").insert(records).execute()
            # await update.message.reply_text(
            #     f"{len(records)} data barang berhasil dismpan "
            # )
            import requests
            response = requests.post(
                settings_id.api_url + "/api/v1/ai/general",
                json=payload,
                headers=headers)
            if response.status_code == 200:
                return response.json()['data']['response']
            else:
                raise ValidationError(response.text())
        context.user_data.pop("mode", None)
    except Exception as e:
        await update.message.reply_text(f"terjadi kesalahan : {e}")
