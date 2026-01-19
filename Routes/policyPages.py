from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter()


def _read_html(filename: str) -> str:
    html_path = Path(__file__).resolve().parent.parent / "components" / filename
    try:
        return html_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return "<html><body><h1>Page not found</h1></body></html>"


@router.get("/privacy-policy", response_class=HTMLResponse)
async def privacy_policy() -> HTMLResponse:
    content = _read_html("privacyPolicy.html")
    return HTMLResponse(content=content, status_code=200)


@router.get("/refund-policy", response_class=HTMLResponse)
async def refund_policy() -> HTMLResponse:
    content = _read_html("refundPolicy.html")
    return HTMLResponse(content=content, status_code=200)


@router.get("/terms-and-conditions", response_class=HTMLResponse)
async def terms_and_conditions() -> HTMLResponse:
    content = _read_html("termsAndConditions.html")
    return HTMLResponse(content=content, status_code=200)
