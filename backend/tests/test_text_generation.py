import pytest
import json
from backend.services.text_generation import TextGenerationService

question_data_path = "./datasets/question_data.json"
answer_data_path = "./datasets/answer_data.json"

with open(question_data_path, "r", encoding="utf-8") as file:
    questions = json.load(file)

with open(answer_data_path, "r", encoding="utf-8") as file:
    answers = {item["answer_id"]: item["answer"] for item in json.load(file)}


@pytest.fixture
def text_generation_service():
    return TextGenerationService()


@pytest.mark.parametrize("question_data", questions)
def test_question_answer_mapping(text_generation_service, question_data):
    question = question_data["question"]
    expected_answer_id = question_data["answer_id"]
    expected_answer = answers[expected_answer_id]

    response = text_generation_service.answer_question(question)
    assert response == expected_answer


def test_empty_question_response(text_generation_service):
    question = ""
    expected_response = "En valitettavasti osaa vastata kysymykseesi."
    response = text_generation_service.answer_question(question)
    assert response == expected_response


def test_invalid_question_response(text_generation_service):
    question = "Mikä on Suomen pääkaupunki?"
    expected_response = "En valitettavasti osaa vastata kysymykseesi."
    response = text_generation_service.answer_question(question)
    assert response == expected_response


def test_question_with_special_characters(text_generation_service):
    with open(answer_data_path, "r", encoding="utf-8") as file:
        answers = json.load(file)
    question = "!Kuka voi saada @ opintotukea=?"
    expected_response = answers[0]["answer"]
    response = text_generation_service.answer_question(question)
    assert response == expected_response
