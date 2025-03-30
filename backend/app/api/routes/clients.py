from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    ClientInfo,
    ClientInfoCreate,
    ClientInfoPublic,
    ClientInfoUpdate,
    Message,
)

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("/", response_model=list[ClientInfoPublic])
def read_clients(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve clients.
    """
    statement = select(ClientInfo).offset(skip).limit(limit)
    clients = session.exec(statement).all()
    return clients


@router.get("/by-apartment/{apt_id}", response_model=list[ClientInfoPublic])
def read_clients_by_apartment(
    session: SessionDep, current_user: CurrentUser, apt_id: int
) -> Any:
    """
    Get clients by apartment ID.
    """
    statement = select(ClientInfo).where(ClientInfo.apt_id == apt_id)
    clients = session.exec(statement).all()
    return clients


@router.get("/{id}", response_model=ClientInfoPublic)
def read_client(session: SessionDep, current_user: CurrentUser, id: int) -> Any:
    """
    Get client by ID.
    """
    client = session.get(ClientInfo, id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.post("/", response_model=ClientInfoPublic)
def create_client(
    *, session: SessionDep, current_user: CurrentUser, client_in: ClientInfoCreate
) -> Any:
    """
    Create new client.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    client = ClientInfo.model_validate(client_in)
    session.add(client)
    session.commit()
    session.refresh(client)
    return client


@router.put("/{id}", response_model=ClientInfoPublic)
def update_client(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: int,
    client_in: ClientInfoUpdate,
) -> Any:
    """
    Update a client.
    """
    client = session.get(ClientInfo, id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_dict = client_in.model_dump(exclude_unset=True)
    client.sqlmodel_update(update_dict)
    session.add(client)
    session.commit()
    session.refresh(client)
    return client


@router.delete("/{id}")
def delete_client(session: SessionDep, current_user: CurrentUser, id: int) -> Message:
    """
    Delete a client.
    """
    client = session.get(ClientInfo, id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    session.delete(client)
    session.commit()
    return Message(message="Client deleted successfully") 