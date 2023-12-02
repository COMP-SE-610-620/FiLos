## Backend Structure

- `Backend`: The backend of the project.
  - `services`: Services for loading and performing tasks using the pre-trained models.
    - `speech_to_text.py`: Service for converting speech to text.
    - `text_to_speech.py`: Service for converting text to speech.
    - `text_generation.py`: Service for generating text.
  - `router`: Contains API routing scripts for defining RESTful API endpoints.
    - `api.py`: Script defining API routes and handling requests.
  - `notebooks`: Jupyter notebooks used for downloading and saving Hugging Face models.
    - `download_model.ipynb`: Notebook for downloading and saving models.
  - `main.py`: The main entry point of the application, responsible for initializing and running the FastAPI server.

## Models
### speech-to-text (Finnish-NLP Group)
Our Speech-to-Text model, developed by the Finnish-NLP Group, is powered by the state-of-the-art Wav2Vec2 architecture. This model excels in converting spoken Finnish language into accurate written text. 
- https://huggingface.co/Finnish-NLP/wav2vec2-large-uralic-voxpopuli-v2-finnish.
### text-generation (TurkuNLP Research Group)
Our Text Generation model, crafted by the TurkuNLP Research Group, utilizes the SBERT (Sentence-BERT) architecture specifically tuned for Finnish language nuances. 
- https://huggingface.co/TurkuNLP/sbert-cased-finnish-paraphrase
### text-to-speech (mozilla/TTS)
Our Text-to-Speech model, named tts_models/fi/css10/vits, is part of the mozilla/TTS project, is designed to convert written text into natural-sounding Finnish speech. 
- https://huggingface.co/facebook/mms-tts-fin.

## Usage instructions

### Docker Installation
To install the system using Docker, ensure Docker is installed and running. Execute the following Docker commands:
```bash
docker-compose build
docker-compose up
```
The server will be accessible at http://127.0.0.1:8000/.

### Local Installation
*Prerequisites:* Python 3.9 & Pip

#### Environment Setup
Create a virtual environment:
```bash
python -m venv env
```

- On Linux/Mac, activate the environment with:

```bash
source env/bin/activate
```

- On Windows, activate the environment with:
```bash
.\env\Scripts\activate
```
- On git bash, activate the environment with:
```bash
source env/Scripts/activate
```

Next, install the required python dependencies using:

```bash
pip install -r requirements.txt
```


#### Run API server

Once the system is installed, you can run the API server with the following command:
```bash
uvicorn main:app --reload
```
The server will be accessible at http://127.0.0.1:8000/.

## API Documentation

The API documentation is available at http://127.0.0.1:8000/docs/. Explore the endpoints and interact with the API using the Swagger documentation.


## Troubleshooting
### Potential Issues
You man encounter the following issues when installing and running the backend locally since dependency-related in your machine
#### Issue 1: Missing Microsoft Visual C++ 14.0 in windows
- **Error Message:** When running `pip install -r requirements.txt` in windows enviroment, you encounter the following error:

- building 'TTS.tts.utils.monotonic_align.core' extension
error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/

-  **How to fix**: Visit [Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) to download and install the tools


#### Issue 2: ModuleNotFoundError 
- **Error Message:** When running `uvicorn main:app --reload
`, you encounter the following error:
- ModuleNotFoundError: No module named 'TTS
- ** How to fix**: Activate the environment again
- - On Mac/Linux: source env/bin/activate
- - On windows: .\env\Scripts\activate

