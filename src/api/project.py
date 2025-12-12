from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.schemas.project import ProjectCreate, ProjectRead
from src.storage.db.db import get_db
from src.storage.db.repositories import ProjectRepository
from src.api.dependencies import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=ProjectRead)
async def create_project(
    project: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    repo = ProjectRepository(db)
    created = await repo.create_project(
        name=project.name,
        owner_id=current_user.id,
        description=project.description
    )
    return created

@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(project_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = ProjectRepository(db)
    project = await repo.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=ProjectRead)
async def update_project(project_id: UUID, project: ProjectCreate, db: AsyncSession = Depends(get_db)):
    repo = ProjectRepository(db)
    updated = await repo.update_project(
        project_id=project_id,
        name=project.name,
        description=project.description
    )
    return updated

@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = ProjectRepository(db)
    await repo.delete_project(project_id)
