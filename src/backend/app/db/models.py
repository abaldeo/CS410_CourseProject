from sqlalchemy import Boolean, Column, Integer, String

from .session import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

class FileUpload(Base):
    __tablename__ = 'file_upload'
    # id = Column(Integer, primary_key=True, index=True)
    course_id = Column(String, index=True)
    course_name = Column(String, nullable=True)
    week_number = Column(String, nullable=True)
    lecture_number = Column(String, nullable=True)
    lecture_title = Column(String, nullable=True)
    source_url = Column(String, nullable=True)
    s3_url = Column(String, primary_key=True, index=True)
    file_name = Column(String)
    doc_type = Column(String)  
    file_md5 = Column(String)	
	