from aiogram import Bot, Dispatcher
from aiogram.types import User, ContentType
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
import random
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.text import (
    Const,
    Format,
)  # Здесь будем импортировать нужные виджеты

from aiogram_dialog.widgets.kbd import (
    Button,
    Select,
    Column,
)  # Здесь будем импортировать нужные виджеты

from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from environs import Env
import logging

logging.basicConfig(level=logging.INFO)

env = Env()
env.read_env()
BOT_TOKEN = env("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


class StartSG(StatesGroup):
    start = State()


class KittenTestSG(StatesGroup):
    start = State()
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()
    result = State()


async def go_start(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)


async def go_kitten_test(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    await dialog_manager.start(state=KittenTestSG.start, mode=StartMode.RESET_STACK)


async def go_next_button(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    await dialog_manager.next()


async def go_next_select(
    callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str
):
    # print(f"Выбрана категория с id={item_id}")
    await dialog_manager.next()


async def some_handler(
    callback: CallbackQuery, dialog_manager: DialogManager
):  # Здесь будут хэндлеры
    pass


async def some_getter(**kwargs):  # Здесь будем создавать нужные геттеры
    pass


async def username_getter(
    dialog_manager: DialogManager, event_from_user: User, **kwargs
):
    return {"username": event_from_user.username}


kittens = [
    ("котёнок-невдуплёныш", "/home/drmrn/test_bot/sources/clear_brain_cat.jpg"),
    ("печальный котейка", "/home/drmrn/test_bot/sources/emo_cat.jpg"),
    ("игривый котик", "/home/drmrn/test_bot/sources/playful_cat.jpg"),
    ("коть-умняшка", "/home/drmrn/test_bot/sources/smart_cat.jpg"),
]


async def kitten_getter(dialog_manager: DialogManager, **kwargs):
    kit = random.choice(kittens)
    print(kit)
    return {
        "kitten_text": kit[0],
        "kitten_image": MediaAttachment(type=ContentType.PHOTO, path=kit[1]),
    }


# Это стартовый диалог
start_dialog = Dialog(
    Window(
        Format(
            "Привет, {username}, не хочешь пройти какой-нибудь тест?"
        ),  # just a constant text
        Button(
            Const("Какой я котик?"), id="kitten_test_button", on_click=go_kitten_test
        ),
        Button(Const("Какой я пёсик?"), id="puppy_test_button"),
        Button(Const("Какой я хомяк?"), id="hamster_test_button"),
        getter=username_getter,
        state=StartSG.start,  # state is used to identify window between dialogs
    )
)

kitten_test_dialog = Dialog(
    Window(
        Const("Давай узнаем, какой ты котик. Чтобы начать, нажми кнопку👇"),
        DynamicMedia("kitten_image"),
        Button(
            Const("Начать тест"), id="kitten_test_start_button", on_click=go_next_button
        ),
        getter=kitten_getter,
        state=KittenTestSG.start,
    ),
    Window(
        Const("Какой у тебя любимый твороженный сырок?"),
        Column(
            Select(
                Format("{item[0]}"),
                id="glazed_cheese",
                item_id_getter=lambda x: x[1],
                items=[
                    ("Шоколадный", 1),
                    ("Ванильный", 2),
                    ("С варённой сгущёнкой", 3),
                    ("Я не люблю сырки :(", 4),
                ],
                on_click=go_next_select,
            ),
        ),
        state=KittenTestSG.q1,
    ),
    Window(
        Const("Твоё любимое время года?"),
        Column(
            Select(
                Format("{item[0]}"),
                id="season",
                item_id_getter=lambda x: x[1],
                items=[
                    ("Зима", 1),
                    ("Весна", 2),
                    ("Лето", 3),
                    ("Осень", 4),
                ],
                on_click=go_next_select,
            ),
        ),
        state=KittenTestSG.q2,
    ),
    Window(
        Const("А что насчёт искусства?"),
        Column(
            Select(
                Format("{item[0]}"),
                id="hobby",
                item_id_getter=lambda x: x[1],
                items=[
                    ("Я настоящий киноман", 1),
                    ("Почти всегда в наушниках", 2),
                    ("Меня можно назвать книжным червём", 3),
                    ("5 лет художки вам о чём-нибудь  говорят?", 4),
                ],
                on_click=go_next_select,
            ),
        ),
        state=KittenTestSG.q3,
    ),
    Window(
        Const("А какой у тебя характер?"),
        Column(
            Select(
                Format("{item[0]}"),
                id="temper",
                item_id_getter=lambda x: x[1],
                items=[
                    ("Я добрая лапочка", 1),
                    ("Я саркастичная штучка", 2),
                    ("Я злюка, а что, нельзя!?", 3),
                    ("Спокойствие - моё второе имя", 4),
                ],
                on_click=go_next_select,
            ),
        ),
        state=KittenTestSG.q4,
    ),
    Window(
        Const("Тебе понравился тест?"),
        Column(
            Select(
                Format("{item[0]}"),
                id="feedback",
                item_id_getter=lambda x: x[1],
                items=[
                    ("Да", 1),
                    ("А как иначе?", 2),
                    ("Хочу еще тестов", 3),
                    ("Первый вариант", 4),
                ],
                on_click=go_next_select,
            ),
        ),
        state=KittenTestSG.q5,
    ),
    Window(
        # TODO: вариативная картиночка
        Format("Поздраваляю, ты - {kitten_text}!"),
        DynamicMedia("kitten_image"),
        Button(Const("В главное меню"), id="to_start_menu", on_click=go_start),
        getter=kitten_getter,
        state=KittenTestSG.result,
    ),
)


# Этот классический хэндлер будет срабатывать на команду /start
@dp.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)


dp.include_routers(start_dialog, kitten_test_dialog)
setup_dialogs(dp)

if __name__ == "__main__":

    dp.run_polling(bot)
