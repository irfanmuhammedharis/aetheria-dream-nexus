# Verified against Section 3 and Phase 1: Persistent models for User and Dream

import uuid
from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from apps.backend.src.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(320), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    dreams = relationship("Dream", back_populates="user")

class Dream(Base):
    __tablename__ = "dreams"

    dream_id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    timestamp_ingested = Column(DateTime(timezone=True), server_default=func.now())
    timestamp_experience = Column(DateTime(timezone=True), nullable=True)
    input_modality = Column(String, nullable=False)
    content_raw = Column(String, nullable=False)
    biometric_context = Column(JSON, nullable=True)
    archetype_id = Column(String, nullable=True)

    user = relationship("User", back_populates="dreams")

# Verification Log
# - Models implement required fields from DreamIngestionObject and user model for auth.
# - Use UUID PKs and JSON column for biometric_context.
# - Assumption: archetype linkage stored as string; vector references kept in Pinecone.