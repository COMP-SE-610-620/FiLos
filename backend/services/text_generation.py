import json
import torch
from transformers import AutoTokenizer, AutoModel
from sentence_transformers.util import semantic_search

MODEL_PATH = "./models/sbert-cased-finnish-paraphrase/0_BERT/"

class TextGenerationService:
    """
    A service for generating text and answering questions using pre-trained models.
    """

    def __init__(self):
        """
        Initializes the TextGenerationService by loading the QA model and data.
        """
        self.qa_model, self.qa_tokenizer = self.load_qa_model()
        (
            self.questions,
            self.answers,
            self.qa_dict,
            self.embedded_questions,
        ) = self.load_qa_data()

    def load_qa_model(self):
        """
        Loads the question-answering model and tokenizer.

        Returns:
            tuple: The QA model and tokenizer.
        """
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        model = AutoModel.from_pretrained(MODEL_PATH)
        return model, tokenizer

    def load_qa_data(self):
        """
        Loads the QA dataset, extracts questions and answers, and embeds the questions.

        Returns:
            tuple: Lists of questions, answers, a dictionary mapping questions to answers,
                   and embeddings of the questions.
        """
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
        """
        Performs mean pooling on the model output.

        Args:
            model_output (torch.Tensor): The output from the transformer model.
            attention_mask (torch.Tensor): The attention mask for the input.

        Returns:
            torch.Tensor: The pooled output.
        """
        token_embeddings = model_output[0]
        input_mask_expanded = (
            attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        )
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
            input_mask_expanded.sum(1), min=1e-9
        )

    def sentence_embedding(self, sentences):
        """
        Computes the sentence embeddings for the given sentences.

        Args:
            sentences (list[str]): A list of sentences.

        Returns:
            torch.Tensor: The sentence embeddings.
        """
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
        """
        Finds the most similar question from the dataset and returns the corresponding answer.

        Args:
            input_question (str): The input question.

        Returns:
            str: The answer to the input question.
        """
        embedded_question = self.sentence_embedding(input_question)
        hit = semantic_search(embedded_question, self.embedded_questions, top_k=1)[0][0]

        if hit["score"] > 0.8:
            closest_question = self.questions[hit["corpus_id"]]
            if closest_question in self.qa_dict:
                return self.qa_dict[closest_question]
            else:
                return "En valitettavasti osaa vastata kysymykseesi."
        else:
            return "En valitettavasti osaa vastata kysymykseesi."
