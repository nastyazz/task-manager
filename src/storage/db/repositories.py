from sqlalchemy.ext.asyncio import AsyncSession 
from src.storage.db.model.models import User, Project, Task, Intergration, Event
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from uuid import UUID
from datetime import datetime
import uuid

class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, project_id: str, title: str, description: str, source: str, external_id) -> Task:
        task = Task(project_id=project_id, title=title, description=description, source=source, external_id=external_id)
        try:
            self.db.add(task)
            await self.db.commit()
            await self.db.refresh(task)
            return task
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise 
        except Exception as e:
            await self.db.rollback()
            raise
    
    async def create_or_update_from_external(self, source: str, external_id: str, repo_full_name: str, title: str, description: str) -> Task:
        intergration = await self.db.scalar(
            select(Intergration)
            .where(Intergration.type == source)
            .where(Intergration.external_id == repo_full_name)
            .where(Intergration.enabled == True)
        )
        if not intergration:
            raise ValueError("No enabled integration found for the given source and repository.")
        
        project_id = intergration.project_id
        
        q = (
            select(Task)
            .where(Task.source == source)
            .where(Task.external_id == external_id)
        )

        result = await self.db.execute(q)
        task = result.scalar_one_or_none()
        if not task:
            task = await self.create_task(title=title, description=description, source=source, external_id=external_id, project_id=project_id)
        else:
            task.title = title
            task.description = description
        
        await self.db.commit()
        return task
    async def update_status_from_external(self, repo_full_name: str, external_id: str, status) -> Task:
        intergration = await self.db.scalar(
            select(Intergration)
            .where(Intergration.type == "github")
            .where(Intergration.external_id == repo_full_name)
            .where(Intergration.enabled == True)
        )
        if not intergration:
            raise ValueError("No enabled integration found for the given source and repository.")
        
        q = (
            select(Task)
            .where(Task.source == "github")
            .where(Task.external_id == external_id)
        )

        result = await self.db.execute(q)
        task = result.scalar_one_or_none()
        if not task:
            raise ValueError("Task not found for the given external ID.")
        
        task.status = status
        await self.db.commit()
        return task
    
    async def delete_task_from_external(self, repo_full_name: str, external_id: str) -> None:
        intergration = await self.db.scalar(
            select(Intergration)
            .where(Intergration.type == "github")
            .where(Intergration.external_id == repo_full_name)
            .where(Intergration.enabled == True)
        )
        if not intergration:
            raise ValueError("No enabled integration found for the given source and repository.")
        
        q = (
            select(Task)
            .where(Task.source == "github")
            .where(Task.external_id == external_id)
        )

        result = await self.db.execute(q)
        task = result.scalar_one_or_none()
        if not task:
            raise ValueError("Task not found for the given external ID.")
        
        await self.db.delete(task)
        await self.db.commit()
        
class ProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_project(self, name: str, owner_id: UUID, description: str | None = None) -> Project:
        project = Project(
            id=uuid.uuid4(),
            name=name,
            owner_id=owner_id,
            description=description,
            created_at=datetime.utcnow()
        )
        self.db.add(project)
        try:
            await self.db.commit()
            await self.db.refresh(project)
            return project
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def get_project_by_id(self, project_id: UUID) -> Project | None:
        try:
            result = await self.db.execute(select(Project).where(Project.id == project_id))
            return result.scalars().first()
        except SQLAlchemyError:
            raise

    async def update_project(self, project_id: UUID, name: str | None = None, description: str | None = None) -> Project:
        project = await self.get_project_by_id(project_id)
        if not project:
            raise ValueError("Project not found")
        if name:
            project.name = name
        if description:
            project.description = description
        await self.db.commit()
        await self.db.refresh(project)
        return project

    async def delete_project(self, project_id: UUID) -> None:
        project = await self.get_project_by_id(project_id)
        if not project:
            raise ValueError("Project not found")
        await self.db.delete(project)
        await self.db.commit()


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_user_by_id(self, user_id: str) -> User | None:
        try:
            res = await self.db.execute(select(User).where(User.id == user_id))
            user = res.scalars().first()
            return user
        except SQLAlchemyError as e:
            raise
        except Exception as e:
            raise
    
    async def get_user_by_username(self, username: str) -> User | None:
        try:
            res = await self.db.execute(select(User).where(User.username == username))
            user = res.scalars().first()
            return user
        except SQLAlchemyError as e:
            raise
        except Exception as e:
            raise
    
    async def create_user(self, username: str, email: str) -> User:
        user = User(username=username, email=email)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_user(self, user_id: str, username: str | None = None, email: str | None = None) -> User:
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        if username:
            user.username = username
        if email:
            user.email = email

        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user_id: str) -> None:
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        await self.db.delete(user)
        await self.db.commit()


class IntegrationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

class EventRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    
   
    