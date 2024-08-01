from pydantic import BaseModel
from typing import override, Iterator
from pydantic_core import from_json
import os
from bot.configs.config import Config
from glob import glob


class Question(BaseModel):
    text: str
    answers: list[str]


class Questions(BaseModel):
    name: str
    description: str
    questions: list[Question]

    def __getitem__(self, index: int) -> Question:
        return self.questions[index]

    @override
    def __iter__(self) -> Iterator[Question]:  # type: ignore
        return self.questions.__iter__()

    def __len__(self) -> int:
        return len(self.questions)


def _questions_from_json(test_path: str) -> Questions:
    with open(test_path, "r") as json_file:
        questions_json = from_json(json_file.read(), cache_strings=True)
    questions = Questions.model_validate(questions_json)

    return questions


def _tests_path(models_path: str):
    return f"{models_path}{os.sep}tests{os.sep}"


def _json_name(json_path: str) -> str:
    """Парсит незвание json файла

    /path/to/file.json -> file"""
    json_name = json_path.split(os.sep)[-1].split(".")[0]

    return json_name


def parse_questions_dict(config: Config) -> dict[str, "Questions"]:
    questions_path = _tests_path(str(config.models_path))

    questions: dict[str, "Questions"] = {}
    for questions_json_path in glob(questions_path + "*"):
        questions_json_name = _json_name(questions_json_path)
        questions_model = _questions_from_json(questions_json_path)
        questions[questions_json_name] = questions_model

    return questions


if __name__ == "__main__":
    ...