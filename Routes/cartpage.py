from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter()


def _read_html_file(filename: str) -> str:
    # Resolve path to components relative to project root
    html_path = Path(__file__).resolve().parent.parent / "components" / filename
    try:
        return html_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"<html><body><h1>{filename} not found</h1></body></html>"


@router.get("/fundamentals-of-facebook-ads/cartpage", response_class=HTMLResponse)
async def cartPage() -> HTMLResponse:
    content = _read_html_file("cartPage.html")
    return HTMLResponse(content=content, status_code=200)


@router.get("/psychology-driven-advanced-meta-ad-course/basic-cart", response_class=HTMLResponse)
async def basicCart() -> HTMLResponse:
    content = _read_html_file("basicCart.html")
    return HTMLResponse(content=content, status_code=200)


@router.get("/psychology-driven-advanced-meta-ad-course/value-cart", response_class=HTMLResponse)
async def valueCart() -> HTMLResponse:
    content = _read_html_file("valueCart.html")
    return HTMLResponse(content=content, status_code=200)


@router.get("/psychology-driven-advanced-meta-ad-course/business-growth-cart", response_class=HTMLResponse)
async def businessGrowthCart() -> HTMLResponse:
    content = _read_html_file("businessGrowthCart.html")
    return HTMLResponse(content=content, status_code=200)


@router.get("/meta-andromeda-update-course/meta-base-cart", response_class=HTMLResponse)
async def metaBaseCart() -> HTMLResponse:
    content = _read_html_file("metaBaseCart.html")
    return HTMLResponse(content=content, status_code=200)


@router.get("/meta-andromeda-update-course/meta-mentorship-cart", response_class=HTMLResponse)
async def metaMentorshipCart() -> HTMLResponse:
    content = _read_html_file("metaMentorshipCart.html")
    return HTMLResponse(content=content, status_code=200)