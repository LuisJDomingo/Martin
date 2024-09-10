from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2

app = FastAPI()

# Conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    dbname="tu_db",
    user="tu_usuario",
    password="tu_password",
    host="localhost"
)
cursor = conn.cursor()

# Modelo para recibir datos de preguntas
class Question(BaseModel):
    question: str

@app.post("/ask/")
def ask_question(question: Question):
    # Aquí procesas la pregunta y generas la respuesta
    if "experiencia" in question.question.lower():
        response = "Tengo 3 años de experiencia en desarrollo backend."
    else:
        response = "No tengo una respuesta para esa pregunta."
    
    return {"response": response}
