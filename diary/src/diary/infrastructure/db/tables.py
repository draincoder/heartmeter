import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, MetaData, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry

from diary.domain.models import Measurement, User

metadata = MetaData()
mapper_registry = registry(metadata=metadata)

user_table = Table(
    "users",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("name", String, nullable=False),
    Column("email", String, nullable=False, unique=True),
    Column("timezone", String, nullable=False),
    Column("birthday", DateTime(timezone=True), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
)

measurement_table = Table(
    "measurements",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), nullable=False),
    Column("systolic", Integer, nullable=False),
    Column("diastolic", Integer, nullable=False),
    Column("pulse", Integer, nullable=False),
    Column("drug", String, nullable=False),
    Column("note", String, nullable=False),
    Column("date", DateTime(timezone=True), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
)

mapper_registry.map_imperatively(User, user_table)
mapper_registry.map_imperatively(Measurement, measurement_table)
