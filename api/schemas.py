from pydantic import BaseModel

class ObjectDetectionBase(BaseModel):
    image_name: str
    class_name: str
    confidence: float
    x_min: float
    y_min: float
    x_max: float
    y_max: float

class ObjectDetectionCreate(ObjectDetectionBase):
    pass

class ObjectDetection(ObjectDetectionBase):
    class Config:
        orm_mode = True