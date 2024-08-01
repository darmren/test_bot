from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from bot.dialogs import start, test_dialog
from bot.states import StartSG

from environs import Env
import logging
from bot.configs.questions import parse_questions_dict, Questions, Question
from bot.configs.config import parse_config

logging.basicConfig(level=logging.INFO)

env = Env()
env.read_env()
BOT_TOKEN = env("BOT_TOKEN")
config = parse_config()
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


# Это стартовый диалог
start_dialog = start.get_dialog()
test_dialog = test_dialog.get_dialog()


# Этот классический хэндлер будет срабатывать на команду /start
@dp.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)


dp.include_routers(start_dialog, test_dialog)
setup_dialogs(dp)
dp["questions_dict"] = parse_questions_dict(config)
dp["config"] = config

if __name__ == "__main__":

    dp.run_polling(bot)
