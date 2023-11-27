import json
from transformers import AutoTokenizer, AutoModel
from sentence_transformers.util import semantic_search
from sentence_transformers import SentenceTransformer

MODEL_PATH = "TurkuNLP/sbert-cased-finnish-paraphrase"

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
            self.q_dict,
            self.a_dict,
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
        Loads the question and answer datasets, extracts questions and answers, and embeds the questions.

        Returns:
            tuple: Lists of questions, a dictionary mapping question indexes to answer_ids, a dictionary mapping answer_ids to answers,
                   and embeddings of the questions.
        """
        questions_path = "./datasets/question_data.json"
        answers_path = "./datasets/answer_data.json"

        with open(questions_path, "r", encoding="utf-8") as file:
            question_data = json.load(file)

        with open(answers_path, "r", encoding="utf-8") as file:
            answer_data = json.load(file)

        questions = []

        # {question index: answer_id}
        q_dict = {}
        # {answer_id: answer}
        a_dict = {}

        for index, item in enumerate(question_data):
            question = item["question"].lower()
            questions.append(question)
            q_dict[index] = item["answer_id"]

        for item in (answer_data):
            answer_id = item["answer_id"]
            answer = item["answer"]
            a_dict[answer_id] = answer

        embedded_questions = self.sentence_embedding(questions)
        return questions, q_dict, a_dict, embedded_questions

    def sentence_embedding(self, sentences):
        """
        Computes the sentence embeddings for the given sentences.

        Args:
            sentences (list[str]): A list of sentences.

        Returns:
            torch.Tensor: The sentence embeddings.
        """
        model = SentenceTransformer('TurkuNLP/sbert-cased-finnish-paraphrase')
        embeddings = model.encode(sentences)
        return embeddings

    def answer_question(self, input_question):
        """
        Finds the most similar question from the dataset and returns the corresponding answer.

        Args:
            input_question (str): The input question.

        Returns:
            str: The answer to the input question.
        """
        embedded_question = self.sentence_embedding(input_question.lower())
        hit = semantic_search(embedded_question, self.embedded_questions, top_k=1)[0][0]

        # Print corpus_id (same as the question index) and cosine similarity score
        #print(hit)

        if hit["score"] > 0.85:
            answer_id = self.q_dict[hit["corpus_id"]]
            answer = self.a_dict[answer_id]
            return answer
        else:
            return "En valitettavasti osaa vastata kysymykseesi."