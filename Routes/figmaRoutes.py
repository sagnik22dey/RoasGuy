from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter()


def _read_html(filename: str) -> str:
    html_path = Path(__file__).resolve().parent.parent / "figma_reference" / filename
    try:
        return html_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return "<html><body><h1>Page not found</h1></body></html>"


@router.get("/desktop", response_class=HTMLResponse)
async def desktop_page() -> HTMLResponse:
    content = _read_html("desktop.html")
    return HTMLResponse(content=content, status_code=200)


@router.get("/thank", response_class=HTMLResponse)
async def thank_page() -> HTMLResponse:
    content = _read_html("thankyou.html")
    return HTMLResponse(content=content, status_code=200)
