from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter()


def _read_courses_html() -> str:
    html_path = Path(__file__).resolve().parent.parent / "components" / "courses.html"
    try:
        return html_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return "<html><body><h1>Courses page not found</h1></body></html>"


@router.get("/courses", response_class=HTMLResponse)
async def courses_page() -> HTMLResponse:
    content = _read_courses_html()
    return HTMLResponse(content=content, status_code=200)
