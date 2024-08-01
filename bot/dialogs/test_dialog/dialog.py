from aiogram_dialog import Dialog, Window
import operator
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import (
    Const,
    Format,
)  # Здесь будем импортировать нужные виджеты
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import (
    Button,
    Select,
    Column,
)
from bot.dialogs.test_dialog.getters import (
    description_getter,
    kitten_getter,
    question_getter,
)
from bot.dialogs.test_dialog.handlers import go_next_button, go_next_select
from bot.states import TestSG, StartSG


async def go_start(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)


def get_dialog() -> Dialog:
    description_window = Window(
        Format("{description}"),
        Button(Const("Начать тест"), id="test_start_button", on_click=go_next_button),
        getter=description_getter,
        state=TestSG.start,
    )
    test_window = Window(
        Format("{text}"),
        Column(
            Select(
                Format("{item[1]}"),
                id="selector",
                item_id_getter=operator.itemgetter(0),
                items="answers",
                on_click=go_next_select,
            ),
        ),
        getter=question_getter,
        state=TestSG.test,
    )
    result_window = Window(
        Format("Поздраваляю, ты - {kitten_text}!"),
        DynamicMedia("kitten_image"),
        Button(Const("В главное меню"), id="to_start_menu", on_click=go_start),  # done?
        getter=kitten_getter,
        state=TestSG.result,
    )

    return Dialog(description_window, test_window, result_window)
