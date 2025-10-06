import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
from flask import Flask
app = Flask(__name__)

# Настройки
BOT_TOKEN = "8007279109:AAEFh17vFWjNmfbnKfN_v4jlI4zzMnOhvCQ"
YOUR_CHAT_ID = "927508173"  # Ваш ID в Telegram

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пересылает все полученные сообщения вам"""
    user = update.message.from_user
    message = update.message

    # Формируем информацию о пользователе
    user_info = f"👤 Пользователь: {user.first_name}"
    if user.last_name:
        user_info += f" {user.last_name}"
    user_info += f" (@{user.username})" if user.username else ""
    user_info += f"\n🆔 ID: {user.id}"

    try:
        # Пересылаем сообщение
        if message.text:
            # Текстовое сообщение
            await context.bot.send_message(
                chat_id=YOUR_CHAT_ID,
                text=f"{user_info}\n\n💬 Сообщение:\n{message.text}"
            )
        elif message.photo:
            # Фото
            await context.bot.send_photo(
                chat_id=YOUR_CHAT_ID,
                photo=message.photo[-1].file_id,
                caption=f"{user_info}\n\n📷 Фото"
            )
        elif message.video:
            # Видео
            await context.bot.send_video(
                chat_id=YOUR_CHAT_ID,
                video=message.video.file_id,
                caption=f"{user_info}\n\n🎥 Видео"
            )
        elif message.document:
            # Документ
            await context.bot.send_document(
                chat_id=YOUR_CHAT_ID,
                document=message.document.file_id,
                caption=f"{user_info}\n\n📄 Документ: {message.document.file_name}"
            )
        elif message.voice:
            # Голосовое сообщение
            await context.bot.send_voice(
                chat_id=YOUR_CHAT_ID,
                voice=message.voice.file_id,
                caption=f"{user_info}\n\n🎤 Голосовое сообщение"
            )

        # Отправляем подтверждение пользователю
        await message.reply_text("")

    except Exception as e:
        logging.error(f": {e}")
        await message.reply_text("")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""




def main():
    """Основная функция"""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавляем обработчики с ПРАВИЛЬНЫМИ фильтрами
    application.add_handler(CommandHandler("start", start_command))

    # Обработчики для разных типов сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message))
    application.add_handler(MessageHandler(filters.PHOTO, forward_message))
    application.add_handler(MessageHandler(filters.VIDEO, forward_message))
    application.add_handler(MessageHandler(filters.Document.ALL, forward_message))  # ПРАВИЛЬНЫЙ фильтр для документов
    application.add_handler(MessageHandler(filters.VOICE, forward_message))

    # Запускаем бота
    print("Бот запущен...")
    application.run_polling()


if __name__ == "__main__":

    main()
