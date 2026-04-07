from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter()


def _read_contactus_html() -> str:
    html_path = Path(__file__).resolve().parent.parent / "components" / "contactUs.html"
    try:
        return html_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return "<html><body><h1>Contact Us page not found</h1></body></html>"

@router.get("/contact-us", response_class=HTMLResponse)
async def contact_us() -> HTMLResponse:
    content = _read_contactus_html()
    return HTMLResponse(content=content, status_code=200)
