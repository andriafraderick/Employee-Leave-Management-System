from sqlalchemy import Table, Column, Integer, String, DateTime
from datetime import datetime
from config.db import metadata, Base
from numbers import Real
from sqlalchemy import Column, String, Boolean, Enum, DateTime, Integer, func, ForeignKey, Float, Text
import enum
from sqlalchemy.orm import relationship

users_1 = Table(
    "users_1",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(50), unique=True, nullable=False, index=True),
    Column("password", String(255), nullable=False),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("updated_at", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
)

student_details = Table(
    "student_details",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
    Column("roll_no", String(50), unique=True, nullable=False),
    Column("class", String(50), nullable=False),
    Column("gender", String(10), nullable=False),
    Column("email_id", String(100), unique=True, nullable=False),
    Column("dob_file_path", String(255), nullable=False)
)

# Role Enum
class RoleEnum(enum.Enum):
    manager = "manager"
    employee = "employee"
    hr = "hr"
    hr_manager = "hr_manager"

# Application Status Enum
class ApplicationStatusEnum(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

# Timestamp Mixin with both created and updated timestamps
class TimestampMixin:
    __abstract__ = True

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class LeaveApplications(Base):
    __tablename__ = "leave_applications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(String, ForeignKey("users.employee_id"), index=True)
    leave_type_id = Column(Integer, ForeignKey("leave_types.id"), index=True)
    date_of_application = Column(DateTime, default=datetime.utcnow)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    manager_id = Column(String, ForeignKey("users.employee_id"), nullable=False, index=True)
    total_days = Column(Float, nullable=False)
    status = Column(Enum(ApplicationStatusEnum), default=ApplicationStatusEnum.pending)
    done_by = Column(String, nullable=True)
    reason = Column(String, nullable=False)
    file_path = Column(String, nullable=True)
    number_of_files = Column(Integer, nullable=True)
    reason_if_rejected = Column(String, nullable=True)

    leave_type_obj = relationship("LeaveTypes", back_populates="leave_applications")
    user_obj = relationship(
        "User",
        back_populates="leave_applications",
        foreign_keys=[employee_id]
    )
    manager_obj = relationship(
        "User",
        back_populates="managed_leave_applications",
        foreign_keys=[manager_id]
    )

# User Model
class User(Base, TimestampMixin):
    __tablename__ = "users"

    employee_id = Column(String, unique=True, index=True, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    designation = Column(String, nullable=False)
    status = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    manager_id = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    leave_details = relationship("LeaveDetails", back_populates="user_obj")
    leave_applications = relationship(
        "LeaveApplications",
        back_populates="user_obj",
        foreign_keys=lambda: [LeaveApplications.employee_id]
    )
    managed_leave_applications = relationship(
        "LeaveApplications",
        back_populates="manager_obj",
        foreign_keys=lambda: [LeaveApplications.manager_id]
    )
    profile = relationship("Profile", back_populates="user", uselist=False)

class LeaveTypes(Base):
    __tablename__ = "leave_types"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    leave_type = Column(String, nullable=False)
    leave_description = Column(String, nullable=False)

    leave_details = relationship("LeaveDetails", back_populates="leave_type_obj")
    leave_applications = relationship("LeaveApplications", back_populates="leave_type_obj")

class LeaveDetails(Base):
    __tablename__ = "leave_details"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(String, ForeignKey("users.employee_id"), index=True)
    leave_type_id = Column(Integer, ForeignKey("leave_types.id"), index=True)

    leave_type_obj = relationship("LeaveTypes", back_populates="leave_details")
    remaining_leaves_obj = relationship("RemainingLeaves", back_populates="leave_detail_obj")
    user_obj = relationship("User", back_populates="leave_details")

class RemainingLeaves(Base):
    __tablename__ = "remaining_leaves"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    leave_detail_id = Column(Integer, ForeignKey("leave_details.id"), index=True)
    total_leaves = Column(Float, nullable=False)
    remaining_leaves = Column(Float, nullable=False)
    year = Column(Integer, nullable=False, default=lambda: datetime.now().year)

    leave_detail_obj = relationship("LeaveDetails", back_populates="remaining_leaves_obj")

# Profile

class Profile(Base):
    __tablename__ = "profiles"

    employee_id = Column(String, ForeignKey("users.employee_id"), primary_key=True, index=True)
    name = Column(String)
    address = Column(String)
    designation = Column(String)
    role = Column(String)
    status = Column(String)
    email = Column(String)
    manager_id = Column(String)
    profile_image = Column(Text, nullable=True)
    gender = Column(String, nullable=True)
    blood_type = Column(String, nullable=True)
    headquarters_address = Column(String, nullable=True)
    office_locations = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    social_links = Column(String, nullable=True)
    specializations = Column(String, nullable=True)
    products_services = Column(String, nullable=True)
    clients_partners = Column(String, nullable=True)
    certifications_awards = Column(String, nullable=True)
    tech_stack = Column(String, nullable=True)
    executives = Column(String, nullable=True)
    open_source_links = Column(String, nullable=True)
    events_hosted = Column(String, nullable=True)
    

    user = relationship("User", back_populates="profile", uselist=False)

