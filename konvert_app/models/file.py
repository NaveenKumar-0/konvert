import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from konvert_app.core.database import Base

class File(Base):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    file_type = Column(String, nullable=False)        # image | video | audio
    original_s3_key = Column(String, nullable=False)
    converted_s3_key = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
