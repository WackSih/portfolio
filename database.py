import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Récupère l'URL de Render (Neon), sinon garde SQLite en local par défaut
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./quiz.db")

# 2. Correction indispensable pour SQLAlchemy qui exige "postgresql://"
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. Création du moteur : SQLite a besoin d'un argument spécial, pas PostgreSQL
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency FastAPI : une session par requête, toujours fermée après."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()