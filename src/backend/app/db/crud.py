from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t

from . import models, schemas
from app.core.security import get_password_hash
from sqlalchemy.dialects.postgresql import insert


def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_by_email(db: Session, email: str) -> schemas.UserBase:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.UserOut]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return user


def edit_user(
    db: Session, user_id: int, user: schemas.UserEdit
) -> schemas.User:
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(user.password)
        del update_data["password"]

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def create_file_upload(db,
                             course_id: str,
                             course_name: str,
                             week_number: str,
                             lecture_number: str,
                             lecture_title: str,
                             source_url: str,
                             s3_url: str,
                             file_name: str,
                             doc_type: str,
                             file_md5: str):
    db_file_upload = models.FileUpload(
        course_id=course_id,
        course_name=course_name,
        week_number=week_number,
        lecture_number=lecture_number,
        lecture_title=lecture_title,
        source_url=source_url,
        s3_url=s3_url,
        file_name=file_name,
        doc_type=doc_type,
        file_md5=file_md5,
    )

    stmt = insert(models.FileUpload).values(
        course_id=course_id,
        course_name=course_name,
        week_number=week_number,
        lecture_number=lecture_number,
        lecture_title=lecture_title,
        source_url=source_url,
        s3_url=s3_url,
        file_name=file_name,
        doc_type=doc_type,
        file_md5=file_md5,
    ).on_conflict_do_update(
        constraint=models.FileUpload.__table__.primary_key,
        set_={
            "course_id": course_id,
            "course_name": course_name,
            "week_number": week_number,
            "lecture_number": lecture_number,
            "lecture_title": lecture_title,
            "source_url": source_url,
            "s3_url": s3_url,
            "file_name": file_name,
            "doc_type": doc_type,
            "file_md5": file_md5,
        }
    )

    await db.execute(stmt)
    await db.commit()
    return db_file_upload



from sqlalchemy.future import select

async def uploaded_file_exists(db , md5_hash: str):
    result = (await db.execute(select(models.FileUpload).filter(models.FileUpload.file_md5 == md5_hash))).scalars().first()
    return result is not None

def delete_file_upload(db: Session, s3_url: str):
    file_upload =  db.query(models.FileUpload).filter(models.FileUpload.s3_url == s3_url).first()
    if not file_upload:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="File not found")
    db.delete(file_upload)
    db.commit()
    return file_upload