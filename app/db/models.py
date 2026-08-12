from sqlalchemy import Column, String, Integer, Float, DateTime, Text
from app.db.database import Base
 
 
class Document(Base):
    __tablename__ = "documents"
 
    id = Column(Integer, primary_key=True)
    file_name = Column(String, nullable=False)
    upload_date = Column(DateTime, nullable=False)
    department = Column(String, nullable=True)
 
 
class Feedback(Base):
    __tablename__ = "feedback"
 
    id = Column(Integer, primary_key=True)
    session_id = Column(String, nullable=False)
    question = Column(Text, nullable=False)
    retrieved_chunks = Column(Text, nullable=True) 
    final_answer = Column(Text, nullable=False)
    feedback = Column(String, nullable=False)  
    timestamp = Column(DateTime, nullable=False)