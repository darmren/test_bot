from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from bot.states import TestSG

from aiogram_dialog.widgets.kbd import (
    Button,
    Select,
)


async def go_next_button(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    await dialog_manager.next()


async def go_next_select(
    callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str
):

    ind = dialog_manager.dialog_data.get("cur_question_ind", 0)
    dialog_manager.dialog_data["cur_question_ind"] = ind + 1
    dialog_name = dialog_manager.start_data["dialog_name"]
    if ind + 1 == len(
        dialog_manager.middleware_data["questions_dict"][dialog_name].questions
    ):
        await dialog_manager.next()
    else:
        await dialog_manager.switch_to(state=TestSG.test)
