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
# ALLOWED_USERS = ['ikbaldes']


# async def  only_for_allowed_user(update:Update, context:ContextTypes.DEFAULT_TYPE):
#     user_id = update.effective_user.username
#     # print(update.effective_user)
#     if user_id not in ALLOWED_USERS:
#         await update.message.reply_text("Mohon maaf anda tidak diizinkan menggunakan bot ini")
#         return False
#     return True
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # if not await only_for_allowed_user(update,context):
    #     return
    await update.message.reply_text(
        f"Halo, {update.effective_user.first_name}! 👋\n"
        "Saya adalah bot financial dari Abeli.\n\n"
        "Silakan gunakan perintah berikut:\n"
        "/tambah_barang — untuk menambah data produk dari file Excel\n"
        "/tambah_keuangan — untuk menambah data keuangan dari file Excel\n"
        "/export_data — untuk mendapatkan data dari database dalam bentuk excel\n\n"
        "Setelah memilih command, kirimkan file Excel (.xlsx) yang sesuai."
    )

# async def tambah_barang(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     context.user_data["mode"] = "barang"
#     await update.message.reply_text(
#         "Silahkan kirim file excel berisi data barang dengan format: nama_product, stock_toko, stock_gudang, stock_kampas"
#     )


# async def tambah_data_keuangan(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     context.user_data["mode"] = "keuangan"
#     await update.message.reply_text("silahkan kirim file excel data keuangan")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Anda mengirim: {update.message.text}")


# handle image
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("jalanji")
    photo = update.message.photo[-1]
    file = await photo.get_file()
    await update.message.reply_photo(
        photo=file.file_id, caption="kamu mengirim gambar ini"
    )


# menu
async def set_commands(app):
    await app.bot.set_my_commands(
        [
            BotCommand("start", "Memulai Bot"),
            BotCommand("/input cost ", ""),
        ]
    )


app = ApplicationBuilder().token(bot_token).post_init(set_commands).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
app.add_handler(MessageHandler(filters.Document.FileExtension("xlsx"), handler_xlsx))
app.add_handler(MessageHandler(filters.PHOTO, handle_image))

# app.add_handler(CommandHandler("data",get_data))
if __name__ == "__main__":
    print("Bot is running...")
    # app.run_webhook(
    #     listen="0.0.0.0",
    #     port=8073,
    #     webhook_url="https://bb31-125-167-115-209.ngrok-free.app/"
    # )

app.run_polling()
