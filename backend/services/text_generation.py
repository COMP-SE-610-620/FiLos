import json
import torch
from transformers import AutoTokenizer, AutoModel
from sentence_transformers.util import semantic_search

MODEL_PATH = "gpt2"


class TextGenerationService:
    def __init__(self):
        self.qa_model, self.qa_tokenizer = self.load_qa_model()
        (
            self.questions,
            self.answers,
            self.qa_dict,
            self.embedded_questions,
        ) = self.load_qa_data()

    def load_qa_model(self):
        tokenizer = AutoTokenizer.from_pretrained(
            "TurkuNLP/sbert-cased-finnish-paraphrase"
        )
        model = AutoModel.from_pretrained("TurkuNLP/sbert-cased-finnish-paraphrase")
        return model, tokenizer

    def load_qa_data(self):
        # Replace with the path to your dataset
        qa_dataset_path = "/backend/kela_dataset.json"
        with open(qa_dataset_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        questions = []
        answers = []
        qa_dict = {}

        for item in data:
            question = item["question"]
            questions.append(question)
            answer = item["answer"]
            answers.append(answer)
            qa_dict[question] = answer

        embedded_questions = self.sentence_embedding(questions)
        return questions, answers, qa_dict, embedded_questions

    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]
        input_mask_expanded = (
            attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        )
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
            input_mask_expanded.sum(1), min=1e-9
        )

    def sentence_embedding(self, sentences):
        encoded_input = self.qa_tokenizer(
            sentences, padding=True, truncation=True, return_tensors="pt"
        )
        with torch.no_grad():
            model_output = self.qa_model(**encoded_input)
        sentence_embeddings = self.mean_pooling(
            model_output, encoded_input["attention_mask"]
        )
        return sentence_embeddings

    def answer_question(self, input_question):
        embedded_question = self.sentence_embedding(input_question)
        hit = semantic_search(embedded_question, self.embedded_questions, top_k=1)[0][0]

        if hit["score"] > 0.7:
            closest_question = self.questions[hit["corpus_id"]]
            if closest_question in self.qa_dict:
                return self.qa_dict[closest_question]
            else:
                return "En valitettavasti osaa vastata kysymykseesi."
        else:
            return "En valitettavasti osaa vastata kysymykseesi."
