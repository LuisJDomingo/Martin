from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Parámetros de conexión
DATABASE_URL = "postgresql://postgres:Genio2712@localhost:5432/chatbot_db"

# Crear el motor de conexión
engine = create_engine(DATABASE_URL)

# Crear una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Metadata para manejar tablas si es necesario
metadata = MetaData()

# Modelo para recibir datos de preguntas
class Question(BaseModel):
    question: str

# Ruta para recibir preguntas
@app.post("/ask/")
def ask_question(question: Question):
    # Crear una sesión
    db = SessionLocal()

    try:
        # Aquí procesas la pregunta y generas la respuesta
        if "experiencia" in question.question.lower():
            response = "Tengo 3 años de experiencia en desarrollo backend."
        else:
            response = "No tengo una respuesta para esa pregunta."

        return {"response": response}
    
    finally:
        # Cerrar la sesión
        db.close()
