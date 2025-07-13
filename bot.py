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
from model.send_file.send_file import handler_income,handler_outcome
# from model.send_file.get_data_to_file import get_data_to_excel

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
        "/cash_masuk — untuk menginput file (excel atau gambar) atau data pemasukan\n"
        "/cash_keluar — untuk menginput file (excel atau gambar) atau data pengeluaran\n"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Anda mengirim: {update.message.text}")


async def input_outcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update.user_data["command"] = "outcome"

    await update.message.reply_text(
        "Silahkan data text, excel, atau gambar"
    )


async def input_income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update.user_data["command"] = "income"

    await update.message.reply_text("Silahkan data text, excel, atau gambar")

async def handler_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_command = update.user_data.get('command')
    if(user_command == 'income'):
        await handler_income(update, context)
    elif(user_command == 'outcome'):
        await handler_outcome(update,context)
    else:
        await update.message.reply_text(" Silahkan gunakan /cash_masuk atau /cash_keluar")
# menu
async def set_commands(app):
    await app.bot.set_my_commands(
        [
            BotCommand("start", "Memulai Bot"),
            BotCommand("/cash_masuk", "Manage data pemasukan"),
            BotCommand("/cash_keluar", "Manage data pengeluaran"),
        ]
    )


app = ApplicationBuilder().token(bot_token).post_init(set_commands).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("cash_masuk", input_income))
app.add_handler(CommandHandler("cash_keluar", input_outcome))
app.add_handler(
    MessageHandler(
        filters.TEXT | filters.PHOTO | filters.Document.FileExtension("xlsx"),
        handler_file,
    )
)

if __name__ == "__main__":
    print("Bot is running...")

app.run_polling()
