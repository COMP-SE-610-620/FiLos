## Backend Structure

- `Backend`: The backend of the project, responsible for processing and managing data.
  - `models`: This directory contains Hugging Face model files for various natural language processing tasks.
    - `facebook_mms_tts_fin`: Model for Multimodal Speech-to-Text synthesis (TTS).
    - `speech_recognition`: Model for automatic speech recognition (ASR).
  - `services`: Services for loading and performing tasks using the pre-trained models.
    - `speech_to_text.py`: Service for converting speech to text.
    - `text_to_speech.py`: Service for converting text to speech.
    - `text_generation.py`: Service for generating text.
  - `router`: Contains API routing scripts for defining RESTful API endpoints.
    - `api.py`: Script defining API routes and handling requests.
  - `notebooks`: Jupyter notebooks used for downloading and saving Hugging Face models.
    - `download_model.ipynb`: Notebook for downloading and saving models.
  - `main.py`: The main entry point of the application, responsible for initializing and running the FastAPI server.




## Environment Setup

*Prerequisites:* Python 3.9 & Pip

```bash
python -m venv env
```

On Linux/Mac, activate the environment with:

```bash
source env/bin/activate
```

On Windows, use:

```bash
.\env\Scripts\activate
```

Next, install the required python dependencies using:

```bash
pip install -r requirements.txt
```


## Run API server

Run server

```bash
uvicorn main:app --reload
```
Once the server is running, it will be accessible at http://127.0.0.1:8000/.

API Documentation will be accessible at http://127.0.0.1:8000/docs/