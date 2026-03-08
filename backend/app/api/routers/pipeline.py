from fastapi import APIRouter

router = APIRouter(prefix="/pipeline", tags=["pipeline"])


@router.get("", summary="Pipeline placeholder")
def get_pipeline_status() -> dict[str, str]:
    return {"message": "pipeline router ready"}
