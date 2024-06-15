from sqlalchemy import Column, Float, String
from api.database import Base

class ObjectDetection(Base):
    __tablename__ = "object_detections"

    image_name = Column(String, primary_key=True, index=True)
    class_name = Column(String, index=True)
    confidence = Column(Float)
    x_min = Column(Float)
    y_min = Column(Float)
    x_max = Column(Float)
    y_max = Column(Float)