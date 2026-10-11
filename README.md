# ResearchMate AI

ResearchMate AI is an AI-powered research assistant that helps students and researchers understand academic papers more efficiently. Built with Python, Streamlit, LangChain, and Google Gemini, it allows users to upload research papers in PDF format, generate structured summaries, and ask questions about the document.

## Features

- **PDF Text Extraction:** Extracts text from uploaded research papers using PyMuPDF.
- **AI-Powered Summarization:** Generates structured summaries covering the research objective, methodology, key findings, limitations, and future research directions.
- **Document-Based Question Answering:** Answers user questions using the content of the uploaded research paper.
- **Structured Outputs:** Uses PydanticOutputParser to organize research summaries into predefined fields.
- **Interactive Web Interface:** Provides a Streamlit interface for uploading documents, generating summaries, and asking questions.
- **Context-Aware Responses:** Instructs the language model to ground answers in the supplied document and acknowledge missing information.

## Tech Stack

- **Language:** Python
- **Frontend:** Streamlit
- **LLM Framework:** LangChain
- **Language Model:** Google Gemini
- **PDF Processing:** PyMuPDF
- **Data Validation:** Pydantic
- **Environment Management:** python-dotenv

## How It Works

1. Upload a research paper in PDF format.
2. ResearchMate AI extracts the text from the document.
3. Choose between generating a structured summary or asking a question.
4. LangChain sends the extracted text and relevant prompt to Google Gemini.
5. The application processes the model's response and displays the result.

## Installation

1. Clone the repository:

   ```bash
   git clone <your-repository-url>
   cd ResearchMate-AI
2. Create Virtual Environment:
   python -m venv .venv
3.Activate the environment:
   ```bash
    .venv\Scripts\Activate.ps1
4. Install dependencies:
   ```bash
      pip install -r requirements.txt
5. Create a .env file in the project root and configure your Google Gemini API key using the environment variable expected by your application.
6.Start the application:
   ```bash
    streamlit run app.py
