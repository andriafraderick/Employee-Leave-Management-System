from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional
from datetime import datetime
from enum import Enum

# ---------------- User Schemas ---------------- #

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  
        validate_by_name = True 

# ---------------- Student Schemas ---------------- #


class StudentBase(BaseModel):
    name: str
    roll_no: str
    class_: str = Field(..., alias="class")
    gender: str
    email_id: str

    class Config:
        populate_by_name = True

class StudentOut(StudentBase):
    id: int
    dob_file_path: str

    class Config:
        from_attributes = True  
        validate_by_name = True 

# ---------------- Tokens ---------------- #

# ✅ Nested user info for token response
class UserInfo(BaseModel):
    employee_id: str
    name: str
    role: str

# ✅ Token response schema
class Token(BaseModel):
    access_token: str
    token_type: str
    user_info: UserInfo
    refresh_token: str  
    role: str 

# ✅ TokenData for JWT decoding
class TokenData(BaseModel):
    employee_id: str
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    

# ✅ Optional: For refresh flow if needed
class RefreshTokenRequest(BaseModel):
    refresh_token: str


# ---------------- Enums ---------------- #

class RoleEnum(str, Enum):
    manager = "manager"
    employee = "employee"
    hr = "hr"
    hr_manager = "hr_manager"

class ApplicationStatusEnum(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

# ---------------- Auth & User ---------------- #

class UserCreate(BaseModel):
    name: str
    employee_id: str
    designation: str
    status: str
    role: RoleEnum
    email: EmailStr
    password: str
    is_active: bool
    manager_id: Optional[str]

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    name: str
    employee_id: str
    designation: str
    status: str
    role: RoleEnum
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    manager_id: Optional[str]

    class Config:
        from_attributes = True  
        validate_by_name = True 

class UserInfo(BaseModel):
    employee_id: str
    name: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_info: UserInfo
    refresh_token: str
    role: str

class TokenData(BaseModel):
    id: Optional[int] = None
    email: Optional[EmailStr] = None

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class PasswordResetRequest(BaseModel):
    email: EmailStr
    current_password: str
    new_password: str

# ---------------- Leave Types ---------------- #

class LeaveTypesBase(BaseModel):
    leave_type: str
    leave_description: str

class LeaveTypeCreate(BaseModel):
    name: str
    description: str | None = None

class LeaveTypesOut(LeaveTypesBase):
    id: int

    class Config:
        from_attributes = True

# ---------------- Leave Details ---------------- #

class LeaveDetailsBase(BaseModel):
    employee_id: str
    leave_type_id: int

class LeaveDetailCreate(LeaveDetailsBase):
    pass

class LeaveDetailsOut(LeaveDetailsBase):
    id: int

    class Config:
        from_attributes = True

# ---------------- Remaining Leaves ---------------- #

class LeaveType(str, Enum):
    CASUAL = "casual"
    SICK = "sick"
    EMERGENCY = "emergency"

class RemainingLeavesBase(BaseModel):
    #employee_id: int
    leave_detail_id: int
    total_leaves: float
    remaining_leaves: float
    year: int
    #leave_type: LeaveType

class RemainingLeaveCreate(BaseModel):
    employee_id: str  # Required to find leave_detail
    leave_type: str   # Required to find leave_detail
    remaining_leaves: float
    total_leaves: float
    year: int

class RemainingLeavesOut(RemainingLeavesBase):
    id: int

    class Config:
        from_attributes = True

class RemainingLeaveUpdate(BaseModel):
    remaining_leaves: Optional[float] = None
    total_leaves: Optional[float] = None

# ---------------- Leave Application ---------------- #

class LeaveApplicationBase(BaseModel):
    employee_id: str
    leave_type_id: int
    start_date: datetime
    end_date: datetime
    manager_id: str
    total_days: float
    status: Optional[ApplicationStatusEnum] = ApplicationStatusEnum.pending
    reason: str
    file_path: Optional[str] = None
    number_of_files: Optional[int] = None
    reason_if_rejected: Optional[str] = None

class LeaveApplicationCreate(LeaveApplicationBase):
    pass

class LeaveApplicationOut(LeaveApplicationBase):
    id: int
    date_of_application: datetime

    class Config:
        from_attributes = True




# ---------------- Profile ---------------- #


class ProfileBase(BaseModel):
    profile_image: Optional[str] = None
    gender: Optional[str]
    blood_type: Optional[str]
    headquarters_address: Optional[str]
    office_locations: Optional[str]
    phone_number: Optional[str]
    social_links: Optional[str]
    specializations: Optional[str]
    products_services: Optional[str]
    clients_partners: Optional[str]
    certifications_awards: Optional[str]
    tech_stack: Optional[str]
    executives: Optional[str]
    open_source_links: Optional[str]
    events_hosted: Optional[str]

class ProfileCreate(ProfileBase):
    employee_id: str
    name: str
    address: str
    designation: str
    role: str
    status: str
    email: str
    manager_id: str

class ProfileUpdate(ProfileBase):
    pass  # Only updatable fields; you can add others here if needed

class ProfileResponse(ProfileCreate):
    class Config:
        orm_mode = True


class LeaveApplyRequest(BaseModel):
    employee_id: str
    leave_type: str = "casual"  # Default to casual leave
    days_applied: int
    clear_lop: bool = True  # Whether to clear LOP days
