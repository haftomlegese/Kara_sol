from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from api import crud, models, schemas
from api.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/object-detections/", response_model=schemas.ObjectDetection)
def create_object_detection(object_detection: schemas.ObjectDetectionCreate, db: Session = Depends(get_db)):
    return crud.create_object_detection(db=db, object_detection=object_detection)

@app.get("/object-detections/", response_model=list[schemas.ObjectDetection])
def read_object_detections(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    object_detections = crud.get_object_detections(db, skip=skip, limit=limit)
    return object_detections

@app.get("/object-detections/{image_name}", response_model=schemas.ObjectDetection)
def read_object_detection(image_name: str, db: Session = Depends(get_db)):
    db_object_detection = crud.get_object_detection_by_image_name(db, image_name=image_name)
    if db_object_detection is None:
        raise HTTPException(status_code=404, detail="Object detection not found")
    return db_object_detection

@app.put("/object-detections/{image_name}", response_model=schemas.ObjectDetection)
def update_object_detection(image_name: str, object_detection: schemas.ObjectDetectionCreate, db: Session = Depends(get_db)):
    db_object_detection = crud.update_object_detection(db, image_name=image_name, object_detection=object_detection)
    if db_object_detection is None:
        raise HTTPException(status_code=404, detail="Object detection not found")
    return db_object_detection

@app.delete("/object-detections/{image_name}", response_model=schemas.ObjectDetection)
def delete_object_detection(image_name: str, db: Session = Depends(get_db)):
    db_object_detection = crud.delete_object_detection(db, image_name=image_name)
    if db_object_detection is None:
        raise HTTPException(status_code=404, detail="Object detection not found")
    return db_object_detection