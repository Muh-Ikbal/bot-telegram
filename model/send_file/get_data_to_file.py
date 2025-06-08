import pandas as pd
import os
from telegram import Update, InputFile
from dotenv import load_dotenv
from telegram.ext import ContextTypes
from config import database
from io import BytesIO


async def get_data_to_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = database.supabase.table("stock_product").select("*").execute()
        data = response.data
        if not data:
            await update.message.reply_text("Data tidak ada")
        df = pd.DataFrame(data)

        output = BytesIO()
        df.to_excel(output, index=False, engine="openpyxl")
        output.seek(0)

        await update.message.reply_document(
            document=InputFile(output, filename="data_product.xlsx"),
            caption="berikut data product dari database",
        )

    except Exception as e:
        await update.message.reply_text(f"Terjadi kesalahan : {e}")
