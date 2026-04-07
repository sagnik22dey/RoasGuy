from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter()


def _read_landingpage_html() -> str:
    # Resolve path to components/landingPage.html relative to project root
    html_path = Path(__file__).resolve().parent.parent / "components" / "landingPage.html"
    try:
        return html_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return "<html><body><h1>Landing Page not found</h1></body></html>"

@router.get("/", response_class=HTMLResponse)
async def landing_page() -> HTMLResponse:
    content = _read_landingpage_html()
    return HTMLResponse(content=content, status_code=200)
