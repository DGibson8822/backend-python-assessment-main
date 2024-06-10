from fastapi import APIRouter

router = APIRouter(
  prefix="/api/health",
  tags=["health"],
)

@router.get("/")
def get_breeds() -> bool:
  return True