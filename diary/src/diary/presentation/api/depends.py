from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header, HTTPException, status


def get_user_id(user_id: str = Header("", alias="user-id")) -> UUID:
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No user-id header found")
    try:
        return UUID(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid UUID format in header") from e


UserID = Annotated[UUID, Depends(get_user_id)]
