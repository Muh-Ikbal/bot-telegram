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
from telegram import BotCommand
from model.send_file.send_file import handler_xlsx
from model.send_file.get_data_to_file import get_data_to_excel

load_dotenv()
bot_token = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Halo, {update.effective_user.first_name}! 👋\n"
        "Saya adalah bot financial dari Abeli.\n\n"
        "Silakan gunakan perintah berikut:\n"
        "📦 /tambah_barang — untuk menambah data *produk* dari file Excel\n"
        "💰 /tambah_keuangan — untuk menambah data *keuangan* dari file Excel\n\n"
        "Setelah memilih command, kirimkan file Excel (.xlsx) yang sesuai."
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
    await update.message.reply_text(
        "Silahkan kirim file excel berisi data barang dengan format: nama_product, stock_toko, stock_gudang, stock_kampas"
    )


async def tambah_data_keuangan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mode"] = "keuangan"
    await update.message.reply_text("silahkan kirim file excel data keuangan")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Anda mengirim: {update.message.text}")


# menu
async def set_commands(app):
    await app.bot.set_my_commands(
        [
            BotCommand("start", "Memulai Bot"),
            BotCommand("/tambah_barang", "Tambah data produk dari Excel"),
            BotCommand("/tambah_keuangan", "Tambah data produ keuangan dari Excel"),
            BotCommand("/export_data", "Export data produk dari database ke excel"),
        ]
    )


app = ApplicationBuilder().token(bot_token).post_init(set_commands).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("tambah_barang", tambah_barang))
app.add_handler(CommandHandler("tambah_keuangan", tambah_data_keuangan))
app.add_handler(CommandHandler("export_data", get_data_to_excel))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
app.add_handler(MessageHandler(filters.Document.FileExtension("xlsx"), handler_xlsx))

# app.add_handler(CommandHandler("data",get_data))
if __name__ == "__main__":
    print("Bot is running...")

app.run_polling()
