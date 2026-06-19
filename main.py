from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os
import PyPDF2

# Load .env file
load_dotenv()

app = FastAPI()

# CORS (so frontend works)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# -----------------------------
# Request model
# -----------------------------
class TextRequest(BaseModel):
    text: str


# -----------------------------
# Helper function
# -----------------------------
def ask_groq(prompt: str):

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    response = completion.choices[0].message.content

    # Clean Markdown formatting
    response = response.replace("**", "")
    response = response.replace("#", "")
    response = response.replace("* ", "• ")
    response = response.replace("*", "")

    return response

# -----------------------------
# Home
# -----------------------------
@app.get("/")
def home():
    return {"message": "API is working 🚀"}


# -----------------------------
# Summarize
# -----------------------------
@app.post("/summarize")
def summarize(request: TextRequest):

    prompt = f"""
You are an expert study assistant.

Summarize the following study notes.

Rules:
- Use simple English.
- Use short sentences.
- Use clear headings.
- Use the • symbol for bullet points.
- Do NOT use Markdown symbols like **, *, # or ```.

Study Notes:
{request.text}
"""

    return {
        "summary": ask_groq(prompt)
    }


# -----------------------------
# Quiz
# -----------------------------
@app.post("/quiz")
def quiz(request: TextRequest):

    prompt = f"""
You are an experienced teacher.

Create exactly 5 multiple-choice questions.

Rules:
- Four options (A, B, C, D)
- Mention the correct answer.
- Keep formatting clean.
- Do NOT use Markdown.

Study Notes:
{request.text}
"""

    return {
        "quiz": ask_groq(prompt)
    }


# -----------------------------
# Explain
# -----------------------------
@app.post("/explain")
def explain(request: TextRequest):

    prompt = f"""
You are a friendly teacher.

Explain the topic in very simple English.

Rules:
- Use easy words.
- Give a real-life example.
- Use small paragraphs.
- Do NOT use Markdown.

Topic:
{request.text}
"""
    return {
        "explanation": ask_groq(prompt)
    }


# -----------------------------
# Form Generator
# -----------------------------
@app.post("/form")
def form(request: TextRequest):

    prompt = f"""
You are an expert form designer.

Create a professional application form.

Include:
Form Title
Description
Fields
Field Types

Keep the layout neat.

Requirement:
{request.text}
"""

    return {
        "form": ask_groq(prompt)
    }


# -----------------------------
# Ask Anything
# -----------------------------
@app.post("/ask")
def ask(request: TextRequest):

    prompt = f"""
You are a helpful AI tutor.

Answer the student's question clearly.

Rules:
- Use simple English.
- Use headings when needed.
- Use • bullets if required.
- Do NOT use Markdown.

Question:
{request.text}
"""

    return {
        "answer": ask_groq(prompt)
    }


# -----------------------------
# PDF Upload + Summary
# -----------------------------
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text


@app.post("/pdf-summary")
async def pdf_summary(file: UploadFile = File(...)):
    print("✅ PDF received")

    pdf_text = extract_text_from_pdf(file.file)
    print("✅ Text extracted")
    print("Characters extracted:", len(pdf_text))

    if not pdf_text.strip():
        return {"summary": "No readable text found in the PDF."}

    pdf_text = pdf_text[:3000]

    print("✅ Sending to Groq")

    answer = ask_groq(prompt=f"""
    You are an expert study assistant.

Summarize the following PDF notes.

Rules:
- Use simple English.
- Use headings.
- Use • bullets.
- Do NOT use Markdown.

Notes:
    {pdf_text}
    """)

    print("✅ Groq replied")

    return {
    "text": pdf_text,
    "summary": answer
}
@app.post("/flashcards")
def flashcards(request: TextRequest):

    prompt = f"""
You are an expert teacher.

Create exactly 5 flashcards.

Format:

Flashcard 1
Question:
Answer:

Flashcard 2
Question:
Answer:

Rules:
- No Markdown.
- Keep formatting clean.

Study Notes:
{request.text}
"""

    return {
        "flashcards": ask_groq(prompt)
    }