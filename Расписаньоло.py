from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from datetime import datetime
import logging

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Расписание для 1-й (нечетной) и 2-й (четной) недели
schedule = {
    # Понедельник (0), Вторник (1), ..., Суббота (5), Воскресенье (6)
    "odd": {  # Нечетная неделя (1-я)
        0: "📅 Понедельник (1-я неделя):\n- ПР Английский (10:45 - 12:15)\n- ЛЕК Основы прграммирования (12:45 - 14:15)",
        1: "📅 Вторник (1-я неделя):\n- ПР История (10:45 - 12:15)\n- ПР Английский (12:45 - 14:15)",
        2: "📅 Среда (1-я неделя):\n- ЛЕК Физра (10:45 - 12:15)\n- ЛЕК Физика (12:45 - 14:15)",
        3: "📅 Четверг (1-я неделя):\n- ЛЕК Математика (10:45 - 12:15)\n- ПР Математика (12:45 - 14:15)\n- ПР Основы программирования (14:30 - 16:00)\n- ЛАБ Цифровое моделирование (16:15 - 17:45)",
        4: "📅 Пятница (1-я неделя):\n- ЛЕК Цифровое моделирование (09:00 - 10:30)\n- ЛЕК История (10:45 - 12:15)\n- ЛЕК Дискретная математика (12:45 - 14:15)",
        5: "📅 Суббота (1-я неделя): Выходной 🎉",
        6: "📅 Воскресенье (1-я неделя): Выходной 🎉"
    },
    "even": {  # Четная неделя (2-я)
        0: "📅 Понедельник (2-я неделя):\n- ПР Основы программирования (10:45 - 12:15)\n- ПР Английский (12:45 - 14:15)",
        1: "📅 Вторник (2-я неделя):\n- ПР Физра (14:30 - 16:00)\n- ПР Основы программирования (16:15 - 17:45)",
        2: "📅 Среда (2-я неделя):\n- ПР Физика (09:00 - 10:30)\n- ЛЕК Физика (10:45 - 12:15)\n- ЛАБ Физика (12:45 - 14:15)",
        3: "📅 Четверг (2-я неделя):\n- ПР Математика (10:45 - 12:15)\n- ЛАБ Цифровое моделирование (12:15 - 14:15)\n- ПР Дискретная математика (14:30 - 16:00)\n- ЛАБ Цифровое моделирование (16:15 - 17:45)",
        4: "📅 Пятница (2-я неделя):\n- ЛЕК История (10:45 - 12:15)\n- ЛЕК Математика (12:45 - 14:15)",
        5: "📅 Суббота (2-я неделя): Выходной 🎉",
        6: "📅 Воскресенье (2-я неделя): Выходной 🎉"
    }
}

def get_week_type():
    """Определяет, четная или нечетная текущая неделя"""
    current_week = datetime.now().isocalendar()[1]  # Номер недели в году
    return "even" if current_week % 2 == 0 else "odd"

def get_tomorrow_schedule():
    today = datetime.now().weekday()  # Текущий день недели (0-6)
    tomorrow = (today + 1) % 7       # День недели завтра
    
    week_type = get_week_type()  # "odd" или "even"
    
    if tomorrow in (5, 6):  # Суббота или воскресенье
        return "Завтра выходной! 🎉"
    else:
        return schedule[week_type][tomorrow]

def r_command(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /rasp"""
    user = update.effective_user
    logger.info(f"Пользователь {user.first_name} запросил расписание.")
    
    schedule_text = get_tomorrow_schedule()
    update.message.reply_text(schedule_text)

def main() -> None:
    """Запуск бота"""
    # ЗАМЕНИТЕ НА РЕАЛЬНЫЙ ТОКЕН ВАШЕГО БОТА
    updater = Updater("TOKEN")

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("rasp", r_command))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
