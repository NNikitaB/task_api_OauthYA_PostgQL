from app.schema import (
    UserCreate, 
    UserGet, 
    UserUpdate,
    UserResponse,
    UserBase,   
    ServiceAccessCreate,
    ServiceAccessUpdate,
    ServiceAccessGet,
    ServiceAccessResponse,
)
from app.models import Users, ServicesAccess
from app.utils.patterns import IUnitOfWork, UnitOfWork
from uuid import UUID



class UserService:
    """Service for working with data of users"""
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_user(self, user_data: UserCreate) -> UserGet:
            """Create new user"""
            async with self.uow:
                new_user = Users(
                    uuid=user_data.uuid,
                    username=user_data.username,
                    psevdonim=user_data.psevdonim,
                    email=user_data.email,
                    email_verified=user_data.email_verified,
                    phone=user_data.phone,
                    hashed_password=user_data.hashed_password,
                    is_active=user_data.is_active,
                    is_superuser=user_data.is_superuser,
                    role=user_data.role,
                    notes=user_data.notes,
                    created_at=user_data.created_at
                )
                await self.uow.users.add(new_user)
                await self.uow.commit()
                return UserGet.model_validate(new_user)

    async def update_user(self,user_data: UserUpdate) -> UserGet:
        """Update existing user"""
        async with self.uow:
            user = await self.uow.users.get_by_identifier(user_data.uuid)
            if user is None:
                raise ValueError("User not found")
            
            for field, value in user_data.model_dump(exclude_unset=True).items():
                setattr(user, field, value)
            await self.uow.users.update(user)
            await self.uow.commit()
            return UserGet.model_validate(user)
        
    async def get_user(self, user_data: UserUpdate) -> UserGet:
        """Get user by UUID"""
        async with self.uow:
            user = await self.uow.users.get_by_identifier(user_data.uuid)
            if user is None:
                raise ValueError("User not found")
            return UserGet.model_validate(user)
        
    async def set_new_password(self,user_data: UserUpdate) -> UserGet:
        """Set new password for user"""
        async with self.uow:
            user = await self.uow.users.get_by_identifier(user_data.uuid)
            if user is None:
                raise ValueError("User not found")
            user.hashed_password = user_data.hashed_password
            await self.uow.users.update(user)
            await self.uow.commit()
            return UserGet.model_validate(user)
        
    async def set_email_verified(self, user_uuid: UUID) -> UserGet:
        """Set email verified for user"""
        async with self.uow:
            user = await self.uow.users.get_by_identifier(user_uuid)
            if user is None:
                raise ValueError("User not found")
            user.email_verified = True
            await self.uow.users.update(user)
            await self.uow.commit()
            return UserGet.model_validate(user)
        
    async def set_email_unverified(self, user_uuid: UUID) -> UserGet:
        """Set email unverified for user"""
        async with self.uow:
            user = await self.uow.users.get_by_identifier(user_uuid)
            if user is None:
                raise ValueError("User not found")
            user.email_verified = False
            await self.uow.users.update(user)
            await self.uow.commit()
            return UserGet.model_validate(user)
        
    async def update_user_role(self, user_data: UserUpdate) -> UserGet:
        """Update user role"""
        async with self.uow:
            user = await self.uow.users.get_by_identifier(user_data.uuid)
            if user is None:
                raise ValueError("User not found")
            user.role = user_data.role
            await self.uow.users.update(user)
            await self.uow.commit()
            return UserGet.model_validate(user)
        
    async def update_user_notes(self, user_data: UserUpdate) -> UserGet:
        """Update user notes"""
        async with self.uow:
            user = await self.uow.users.get_by_identifier(user_data.uuid)
            if user is None:
                raise ValueError("User not found")
            if user_data.notes is None:
                raise ValueError("User notes is None")
            user.notes = user_data.notes
            await self.uow.users.update(user)
            await self.uow.commit()
            return UserGet.model_validate(user)
    
    async def update_email(self, user_data: UserUpdate) -> UserGet:
        """Update user email"""
        async with self.uow:
            user = await self.uow.users.get_by_identifier(user_data.uuid)
            users_email = await self.uow.users.list(filters={"email":user_data.email})
            if users_email:
                raise ValueError("Email already exists other user")
            if user is None:
                raise ValueError("User not found")
            user.email = user_data.email
            await self.uow.users.update(user)
            await self.uow.commit()
            return UserGet.model_validate(user)
        
    async def update_username(self, user_data: UserUpdate) -> UserGet:
        """Update user username"""
        async with self.uow:
            user = await self.uow.users.get_by_identifier(user_data.uuid)
            if user is None:
                raise ValueError("User not found")
            user.username = user_data.username
            await self.uow.users.update(user)
            await self.uow.commit()
            return UserGet.model_validate(user)
        
    async def update_psevdonim(self, user_data: UserUpdate) -> UserGet:
        """Update user psevdonim"""
        async with self.uow:
            user = await self.uow.users.get_by_identifier(user_data.uuid)
            if user is None:
                raise ValueError("User not found")
            user_psevdonim = await self.uow.users.get_by_psevdonim(user_data.psevdonim)
            if user_psevdonim:
                raise ValueError("Psevdonim already exists other user")
            user.psevdonim = user_data.psevdonim
            await self.uow.users.update(user)
            await self.uow.commit()
            return UserGet.model_validate(user)

    async def delete_user(self, user_uuid: UUID) -> None:
        """Delete user by UUID"""
        async with self.uow:
            await self.uow.users.delete(user_uuid)
            await self.uow.commit()

    async def activate_user(self, user_uuid: UUID) -> UserGet:
        """Activate user"""
        async with self.uow:
            user = await self.uow.users.activate_user(user_uuid)
            await self.uow.commit()
            return UserGet.model_validate(user)

    async def deactivate_user(self, user_uuid: UUID) -> UserGet:
        """Deactivate user"""
        async with self.uow:
            user = await self.uow.users.deactivate_user(user_uuid)
            await self.uow.commit()
            return UserGet.model_validate(user)
        
    async def add_service(self,user_data: UserBase,servise_data: ServiceAccessCreate) -> UserGet:
        """Add service to user"""
        async with self.uow:
            user = await self.uow.users.get_by_identifier(user_data.uuid)
            if user is None:
                raise ValueError("User not found")
            sers =  user.services_access
            if servise_data.service_name in sers:
                raise ValueError("Service already exists")
            servise = ServicesAccess(
                service_name=servise_data.service_name,
                user_uuid=servise_data.user_uuid,
                is_active=servise_data.is_active,
                access_level=servise_data.access_level
                )
            await self.uow.services_access.add(servise)
            await self.uow.commit()
            user = await self.uow.users.get_by_identifier(user_data.uuid)
            return UserGet.model_validate(user)
        
    async def delete_service(self,user_data: UserBase,servise_id: int) -> UserGet:
        """Delete service from user"""
        async with self.uow:
            ser = await self.uow.services_access.get_by_identifier(servise_id)
            if ser is None:
                raise ValueError("Service not found")
            if ser.user_uuid == user_data.uuid:
                raise ValueError("User not have this service")
            await self.uow.services_access.delete(servise_id)
            await self.uow.commit()
            user = await self.uow.users.get_by_identifier(user_data.uuid)
            return UserGet.model_validate(user)
    async def update_service(self,user_data: UserBase,servise_data: ServiceAccessUpdate) -> UserGet:
        """Update service"""
        async with self.uow:
            ser = await self.uow.services_access.get_by_identifier(servise_data.id)
            if ser is None:
                raise ValueError("Service not found")
            if ser.user_uuid == user_data.uuid:
                raise ValueError("User not have this service")
            ser.access_level = servise_data.access_level
            ser.is_active = servise_data.is_active
            await self.uow.services_access.update(ser)
            await self.uow.commit()
            user = await self.uow.users.get_by_identifier(user_data.uuid)
            return UserGet.model_validate(user)
        

        



