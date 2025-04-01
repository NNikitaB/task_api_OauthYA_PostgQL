from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum
from .Base import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from uuid import UUID,uuid4
from datetime import datetime, UTC


class ServiceName(Enum):
    """
    Enumeration of available service names in the application.
    
    Defines the unique identifiers for different services that can be accessed,
    including time series analysis, preprocessing, donation, computer vision,
    and advertisement services.
    """
    TimeSeries = "service_TimeSeries"
    PreprocessingTable = "service_PreprocesingTable"
    Donate = "service_Donate"
    ComputerVision = "service_ComputerVision"
    Advertisement = "service_Advertisement"


class AccessLevel(Enum):
    """
    Enumeration representing different access levels for service permissions.
    
    Defines the hierarchy of user access levels in the application:
    - User: Standard access level with basic permissions
    - Pro: Enhanced access level with additional privileges
    - Admin: Highest access level with full system permissions
    """
        
    User = "user"
    Pro = "pro"
    Admin = "admin"


class ServicesAccess(Base):
    """
    Represents a service access record in the database, tracking user permissions for specific services.
    
    This model defines the relationship between users and their access to different services,
    including the service name, activation status, access level, and timestamp of access grant.
    
    Attributes:
        id (int): Primary key for the service access record.
        service_name (ServiceName): The specific service being accessed.
        is_active (bool): Indicates whether the service access is currently active.
        access_level (AccessLevel): The user's permission level for the service.
        granted_at (datetime): Timestamp when the service access was granted.
        user_uuid (UUID): Foreign key linking to the associated user.
    """
        
    __tablename__ = "service_access"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_name: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=False)
    access_level: Mapped[str] = mapped_column(nullable=False,default=AccessLevel.User)
    granted_at = mapped_column(DateTime, default=datetime.now(UTC))
    user_uuid: Mapped[UUID] = mapped_column(ForeignKey("users.uuid",ondelete="CASCADE"), nullable=False)

    user = relationship("Users", back_populates="services_access")

