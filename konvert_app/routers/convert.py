from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from io import BytesIO
from PIL import Image

from konvert_app.core.security import get_current_user_id
from konvert_app.core.database import SessionLocal
from konvert_app.models.file import File as FileModel

from konvert_app.services.s3 import upload_file, generate_download_url
from konvert_app.services.video_converter import (
    convert_video_to_mp3,
    get_video_duration,
)

router = APIRouter(tags=["Convert"])



# -----------------------------
# DB dependency
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================================
# IMAGE → MULTI FORMAT
# =========================================================
@router.post("/image")
async def convert_image(
    file: UploadFile = File(...),
    format: str = Form(...),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    allowed_input = ["image/jpeg", "image/png", "image/webp"]
    allowed_output = ["pdf", "png", "jpg", "jpeg", "webp", "gif"]

    if file.content_type not in allowed_input:
        raise HTTPException(400, detail="Unsupported image type")

    if format.lower() not in allowed_output:
        raise HTTPException(400, detail="Unsupported output format")

    image_bytes = await file.read()

    # Upload original image
    original_key = upload_file(
        file_bytes=image_bytes,
        filename=file.filename,
        content_type=file.content_type,
        folder="originals/images",
    )

    # Convert image
    img = Image.open(BytesIO(image_bytes))
    output_buffer = BytesIO()

    if format.lower() == "pdf":
        img.convert("RGB").save(output_buffer, format="PDF")
        output_content_type = "application/pdf"
        output_ext = "pdf"
    else:
        img.save(output_buffer, format=format.upper())
        output_content_type = f"image/{format.lower()}"
        output_ext = format.lower()

    output_bytes = output_buffer.getvalue()

    # Upload converted image
    converted_key = upload_file(
        file_bytes=output_bytes,
        filename=file.filename.rsplit(".", 1)[0] + f".{output_ext}",
        content_type=output_content_type,
        folder="converted/images",
    )

    # Save DB record
    record = FileModel(
        user_id=user_id,
        file_type="image",
        original_s3_key=original_key,
        converted_s3_key=converted_key,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "file_id": str(record.id),
        "original_file": generate_download_url(original_key),
        "converted_file": generate_download_url(converted_key),
    }


# =========================================================
# VIDEO → MP3 (unchanged)
# =========================================================
@router.post("/video-to-mp3")
async def video_to_mp3(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    if file.content_type not in ["video/mp4", "video/mov", "video/x-matroska"]:
        raise HTTPException(status_code=400, detail="Unsupported video type")

    video_bytes = await file.read()

    duration = get_video_duration(video_bytes)
    if duration > 30:
        raise HTTPException(status_code=400, detail="Video must be 30 seconds or less")

    original_key = upload_file(
        file_bytes=video_bytes,
        filename=file.filename,
        content_type=file.content_type,
        folder="originals/videos",
    )

    mp3_bytes = convert_video_to_mp3(video_bytes)

    mp3_key = upload_file(
        file_bytes=mp3_bytes,
        filename=file.filename.rsplit(".", 1)[0] + ".mp3",
        content_type="audio/mpeg",
        folder="converted/audio",
    )

    record = FileModel(
        user_id=user_id,
        file_type="video",
        original_s3_key=original_key,
        converted_s3_key=mp3_key,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "file_id": str(record.id),
        "original_file": generate_download_url(original_key),
        "converted_file": generate_download_url(mp3_key),
    }


# =========================================================
# HISTORY
# =========================================================
@router.get("/my-files")
def my_files(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    files = (
        db.query(FileModel)
        .filter(FileModel.user_id == user_id)
        .order_by(FileModel.created_at.desc())
        .all()
    )

    return [
        {
            "id": str(f.id),
            "file_type": f.file_type,
            "original_file": generate_download_url(f.original_s3_key),
            "converted_file": generate_download_url(f.converted_s3_key),
            "created_at": f.created_at,
        }
        for f in files
    ]
