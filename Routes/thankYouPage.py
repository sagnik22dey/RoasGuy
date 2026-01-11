from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter()


def _read_thankYouPage_html() -> str:
    # Resolve path to components/homepage.html relative to project root
    html_path = Path(__file__).resolve().parent.parent / "components" / "thankYouPage.html"
    try:
        return html_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return "<html><body><h1>Thank You Page not found</h1></body></html>"


@router.get("/thankyou", response_class=HTMLResponse)
async def thankYouPage() -> HTMLResponse:
    content = _read_thankYouPage_html()
    return HTMLResponse(content=content, status_code=200)


def _read_metaThankyou_html() -> str:
    # Resolve path to components/metaThankyou.html relative to project root
    html_path = Path(__file__).resolve().parent.parent / "components" / "metaThankyou.html"
    try:
        return html_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return "<html><body><h1>Meta Thank You Page not found</h1></body></html>"


@router.get("/meta-thank-you", response_class=HTMLResponse)
async def metaThankYouPage() -> HTMLResponse:
    content = _read_metaThankyou_html()
    return HTMLResponse(content=content, status_code=200)