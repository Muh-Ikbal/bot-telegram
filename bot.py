from telegram import Update
import os
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from telegram.constants import ChatAction
from model.send_file.send_file import handler_xlsx

load_dotenv()
bot_token = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Halo, {update.effective_user.first_name}! saya bot financial dari abeli, silakan kirim pesan apapun!"
    )


# async def get_data(update:Update, context: ContextTypes.DEFAULT_TYPE):
#     try:
#         response = supabase.table("stock_product").select("*").execute()
#         data = response.data
#         print(data)
#         if not data:
#             await update.message.reply_text(
#                 "Data tidak ditemukan"
#             )
#             return
#         message = "Laporan Product : \n"
#         for row in data:
#             total_stock = row["stock_toko"] + row["stock_gudang"] + row["stock_kampas"]
#             message += f"""
#             ========================\n
#             Nama : {row["nama_product"]} \n
#             Stock : {total_stock}\n
#             ========================\n
#             """
#         await update.message.reply_text(message)
#     except Exception as e:
#         await update.message.reply_text(f"Gagal mengirim data {e}")


async def tambah_barang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mode"] = "barang"
    await update.message.reply_text("Silahkan kirim file excel berisi data barang")


async def tambah_data_keuangan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mode"] = "keuangan"
    await update.message.reply_text("silahkan kirim file excel data keuangan")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Anda mengirim: {update.message.text}")


app = ApplicationBuilder().token(bot_token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("tambah_barang", tambah_barang))
app.add_handler(CommandHandler("tambah_keuangan", tambah_data_keuangan))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
app.add_handler(MessageHandler(filters.Document.FileExtension("xlsx"), handler_xlsx))

# app.add_handler(CommandHandler("data",get_data))
if __name__ == "__main__":
    print("Bot is running...")

app.run_polling()
