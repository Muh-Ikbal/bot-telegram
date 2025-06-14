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
        "Saya adalah bot management EBITDA.\n\n"
        "Silakan gunakan perintah berikut:\n"
        "/input_file_cost — untuk menginput file cost dalam bentuk file Excel\n"
    )

async def input_file_cost(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mode"] = "barang"
    await update.message.reply_text(
        "Silahkan kirim file excel dengan format .xlsx"
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Anda mengirim: {update.message.text}")


# handle image
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            BotCommand("/input_file_cost", "Tambah data operational dari Excel"),
        ]
    )


app = ApplicationBuilder().token(bot_token).post_init(set_commands).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("input_file_cost", input_file_cost)) #refactor

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
app.add_handler(MessageHandler(filters.Document.FileExtension("xlsx"), handler_xlsx))
app.add_handler(MessageHandler(filters.PHOTO, handle_image))

if __name__ == "__main__":
    print("Bot is running...")
  
app.run_polling()
