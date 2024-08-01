from aiogram.types import ContentType
from aiogram_dialog import DialogManager
import random
from aiogram_dialog.api.entities import MediaAttachment
from bot.configs.questions import Question, Questions

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


async def description_getter(dialog_manager: DialogManager, **kwargs):
    dialog_name = dialog_manager.start_data["dialog_name"]
    questions: Questions = dialog_manager.middleware_data["questions_dict"][dialog_name]
    return {"description": questions.description}


async def question_getter(dialog_manager: DialogManager, **kwargs):
    dialog_name = dialog_manager.start_data["dialog_name"]
    questions = dialog_manager.middleware_data["questions_dict"][dialog_name]
    cur_quesion_ind = dialog_manager.dialog_data.get("cur_question_ind", 0)
    question: Question = questions[cur_quesion_ind]
    return {
        "text": question.text,
        "answers": [(i + 1, answer) for i, answer in enumerate(question.answers)],
        "cur_question_ind": cur_quesion_ind,
    }
