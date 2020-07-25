from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/notes", response_model=schemas.Note, status_code=201)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    return crud.create_note(db=db, note=note)

@app.get("/notes", response_model=List[schemas.Note])
def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    notes = crud.get_notes(db=db, skip=skip, limit=limit)
    return notes

@app.get("/notes/{note_id}", response_model=schemas.Note)
def read_user(note_id: int, db: Session = Depends(get_db)):
    db_note = crud.get_note(db=db, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note

@app.delete("/notes/{note_id}", status_code=204)
async def delete_note(note_id: int, db: Session = Depends(get_db)):    
    return crud.delete_note(db=db, note_id=note_id)


@app.put("/notes/{note_id}", status_code=200)
async def put_note(note_id: int, note: schemas.NoteCreate, db: Session = Depends(get_db)):
    db_note = Note(id = note_id, text = note.text)
    crud.update_note(db=db, note=db_note)

@app.patch("/notes/{note_id}", status_code=200)
async def patch_note(note_id: int, note: schemas.NoteCreate, db: Session = Depends(get_db)):
    print(note_id)
    print(note.text)
    db_note = schemas.Note(id = note_id, text = note.text)
    crud.update_note(db=db, note=db_note)

