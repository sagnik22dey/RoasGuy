from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter()

_BASE = Path(__file__).resolve().parent.parent / "components"


def _read_html(filename: str) -> str:
    try:
        return (_BASE / filename).read_text(encoding="utf-8")
    except FileNotFoundError:
        return "<html><body><h1>Page not found</h1></body></html>"


@router.get("/fundamentals-of-facebook-ads/students", response_class=HTMLResponse)
async def fofa_students() -> HTMLResponse:
    return HTMLResponse(content=_read_html("homepage_students.html"), status_code=200)


@router.get("/fundamentals-of-facebook-ads/business-owners", response_class=HTMLResponse)
async def fofa_business_owners() -> HTMLResponse:
    return HTMLResponse(content=_read_html("homepage_business_owners.html"), status_code=200)
