from bot.dialogs.start.getters import username_getter
from bot.states import StartSG, TestSG
from aiogram_dialog.dialog import Dialog
from aiogram_dialog import Dialog, Window
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.text import (
    Const,
    Format,
)

from aiogram_dialog.widgets.kbd import (
    Button,
    Start,
)


async def go_start(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)


def get_dialog() -> Dialog:
    start_window = Window(
        Format("Привет, {username}, не хочешь пройти какой-нибудь тест?"),
        Start(
            Const("Какой я котик?"),
            id="kitten_test_button",
            state=TestSG.start,
            data={"dialog_name": "kitten_test"},
        ),
        Button(Const("Какой я пёсик?"), id="puppy_test_button"),
        Button(Const("Какой я хомяк?"), id="hamster_test_button"),
        getter=username_getter,
        state=StartSG.start,
    )

    return Dialog(start_window)
