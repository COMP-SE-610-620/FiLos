# cased Finnish Sentence BERT model

Finnish Sentence BERT trained from FinBERT

## Training

    FinBERT model: TurkuNLP/bert-base-finnish-cased-v1
    Data: The data provided [here] (https://turkunlp.org/paraphrase.html), including the Finnish Paraphrase Corpus and the automatically collected paraphrase candidates (500K positive and 5M negative)
    Pooling: mean pooling
    Task: Binary prediction, whether two sentences are paraphrases or not. Note: the labels 3 and 4 are considered paraphrases, and labels 1 and 2 non-paraphrases. [Details on labels] (https://aclanthology.org/2021.nodalida-main.29/)

## Usage

Please refer to the [HuggingFace documentation] (https://huggingface.co/sentence-transformers/bert-base-nli-mean-tokens)

Briefly, using the `SentenceTransformer` library,

```
from sentence_transformers import SentenceTransformer
sentences = ["Tämä on esimerkkilause.", "Tämä on toinen lause."]

model = SentenceTransformer('sbert-cased-finnish-paraphrase')
embeddings = model.encode(sentences)
print(embeddings)
```
