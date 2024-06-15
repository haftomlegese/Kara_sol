from sqlalchemy.orm import Session
from api import models, schemas

# Create a new object detection entry
def create_object_detection(db: Session, object_detection: schemas.ObjectDetectionCreate):
    db_object_detection = models.ObjectDetection(**object_detection.dict())
    db.add(db_object_detection)
    db.commit()
    db.refresh(db_object_detection)
    return db_object_detection

# Read all object detection entries
def get_object_detections(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.ObjectDetection).offset(skip).limit(limit).all()

# Read a single object detection entry by image_name
def get_object_detection_by_image_name(db: Session, image_name: str):
    return db.query(models.ObjectDetection).filter(models.ObjectDetection.image_name == image_name).first()

# Update an object detection entry
def update_object_detection(db: Session, image_name: str, object_detection: schemas.ObjectDetectionCreate):
    db_object_detection = db.query(models.ObjectDetection).filter(models.ObjectDetection.image_name == image_name).first()
    if db_object_detection:
        for key, value in object_detection.dict().items():
            setattr(db_object_detection, key, value)
        db.commit()
        db.refresh(db_object_detection)
    return db_object_detection

# Delete an object detection entry
def delete_object_detection(db: Session, image_name: str):
    db_object_detection = db.query(models.ObjectDetection).filter(models.ObjectDetection.image_name == image_name).first()
    if db_object_detection:
        db.delete(db_object_detection)
        db.commit()
    return db_object_detection