from fastapi import APIRouter

router = APIRouter(prefix="/exports", tags=["exports"])


@router.get("", summary="Exports placeholder")
def list_exports() -> dict[str, str]:
    return {"message": "exports router ready"}
