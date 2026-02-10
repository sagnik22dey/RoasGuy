"""
Graphy Platform Integration Service.

Handles learner creation and course enrollment via Graphy's REST API.
API Base: https://api.ongraphy.com/public/v1/

Endpoints used:
    - POST /learners       -> Create a new learner account
    - POST /assign         -> Enroll learner in a course/package and record external payment
"""

import httpx
import os
import re
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

GRAPHY_API_BASE = "https://api.ongraphy.com/public/v1"
GRAPHY_MID = os.getenv("GRAPHY_MID")
GRAPHY_API_KEY = os.getenv("GRAPHY_API_KEY")

COURSE_GRAPHY_PRODUCT_MAP = {
    "fundamentals-of-facebook-ads": os.getenv("GRAPHY_PRODUCT_FUNDAMENTALS", ""),
    "business-growth-plan": os.getenv("GRAPHY_PRODUCT_BUSINESS_GROWTH", ""),
    "value-plan": os.getenv("GRAPHY_PRODUCT_VALUE_PLAN", ""),
    "meta-andromeda-base": os.getenv("GRAPHY_PRODUCT_META_BASE", ""),
    "meta-andromeda-mentorship": os.getenv("GRAPHY_PRODUCT_META_MENTORSHIP", ""),
}


def _sanitize_phone(phone: str) -> str:
    """
    Clean phone number to ensure single country code prefix.
    Handles cases like '+91+919064292887' → '+919064292887'.
    """
    if not phone:
        return ""
    digits = re.sub(r"[^\d]", "", phone)
    if digits.startswith("91") and len(digits) > 10:
        digits = digits[len(digits) - 10:]
    if len(digits) == 10:
        return f"+91{digits}"
    if phone.startswith("+") and len(digits) > 10:
        return f"+{digits}"
    return f"+{digits}" if digits else ""


async def create_learner(email: str, name: str, phone: str = "") -> dict:
    """
    Create a new learner account on Graphy.

    Args:
        email: Learner's email address.
        name: Learner's full name.
        phone: Learner's phone number with country code (e.g., +917503411234).

    Returns:
        dict with keys 'success' (bool) and 'data' or 'error'.
    """
    if not GRAPHY_MID or not GRAPHY_API_KEY:
        logger.error("Graphy credentials not configured (GRAPHY_MID / GRAPHY_API_KEY)")
        return {"success": False, "error": "Graphy credentials not configured"}

    payload = {
        "mid": GRAPHY_MID,
        "key": GRAPHY_API_KEY,
        "email": email,
        "name": name,
        "sendEmail": "true",
    }

    clean_phone = _sanitize_phone(phone)
    if clean_phone:
        payload["mobile"] = clean_phone

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{GRAPHY_API_BASE}/learners",
                data=payload,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

        response_data = response.json()
        logger.info(f"Graphy Create Learner response [{response.status_code}]: {response_data}")

        if response.status_code == 200 and "error" not in response_data:
            return {"success": True, "data": response_data}
        else:
            error_msg = response_data.get("error", {}).get("message", response.text) if isinstance(response_data.get("error"), dict) else response.text
            return {
                "success": False,
                "error": f"Graphy Create Learner error: {error_msg}",
            }
    except Exception as e:
        logger.error(f"Graphy Create Learner failed: {str(e)}")
        return {"success": False, "error": str(e)}


async def assign_course(
    email: str,
    course_id: str,
    razorpay_payment_id: str,
    phone: str = "",
    country_code: str = "IN",
) -> dict:
    """
    Enroll a learner in a specific course/package on Graphy and record the external payment.

    Args:
        email: Learner's email address.
        course_id: Internal course ID (maps to Graphy productId).
        razorpay_payment_id: The Razorpay payment ID to record in Graphy.
        phone: Learner's phone number (optional).
        country_code: Country code (IN, US, etc.).

    Returns:
        dict with keys 'success' (bool) and 'data' or 'error'.
    """
    if not GRAPHY_MID or not GRAPHY_API_KEY:
        logger.error("Graphy credentials not configured (GRAPHY_MID / GRAPHY_API_KEY)")
        return {"success": False, "error": "Graphy credentials not configured"}

    product_id = COURSE_GRAPHY_PRODUCT_MAP.get(course_id)
    if not product_id:
        logger.error(f"No Graphy product ID mapped for course: {course_id}")
        return {"success": False, "error": f"No Graphy product ID for course: {course_id}"}

    payload = {
        "mid": GRAPHY_MID,
        "key": GRAPHY_API_KEY,
        "email": email,
        "productId": product_id,
        "extPG": "razorpay",
        "extPaymentId": razorpay_payment_id,
    }

    clean_phone = _sanitize_phone(phone)
    if clean_phone:
        payload["phone"] = clean_phone

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{GRAPHY_API_BASE}/assign",
                data=payload,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

        response_data = response.json()
        logger.info(f"Graphy Assign Course response [{response.status_code}]: {response_data}")

        if response.status_code == 200 and "error" not in response_data:
            return {"success": True, "data": response_data}
        else:
            error_msg = response_data.get("error", {}).get("message", response.text) if isinstance(response_data.get("error"), dict) else response.text
            return {
                "success": False,
                "error": f"Graphy Assign Course error: {error_msg}",
            }
    except Exception as e:
        logger.error(f"Graphy Assign Course failed: {str(e)}")
        return {"success": False, "error": str(e)}


async def create_and_enroll_learner(
    email: str,
    name: str,
    phone: str,
    course_id: str,
    razorpay_payment_id: str,
    country_code: str = "IN",
) -> dict:
    """
    Full flow: Create a learner on Graphy, then enroll them in the purchased course.

    This is the main function to call after a successful Razorpay payment.

    Args:
        email: Learner's email address.
        name: Learner's full name.
        phone: Learner's phone with country code.
        course_id: Internal course ID from the payment request.
        razorpay_payment_id: Razorpay payment ID for recording in Graphy.
        country_code: Country code (default: IN).

    Returns:
        dict with 'learner_created', 'course_assigned', and details.
    """
    result = {
        "learner_created": False,
        "course_assigned": False,
        "learner_response": None,
        "assign_response": None,
    }

    learner_result = await create_learner(email=email, name=name, phone=phone)
    result["learner_response"] = learner_result
    result["learner_created"] = learner_result.get("success", False)

    if not learner_result.get("success"):
        error_msg = learner_result.get("error", "")
        if "mobile number is already registered" in error_msg.lower() or "phone" in error_msg.lower():
            logger.warning(
                f"Phone conflict for {email}, retrying learner creation without phone number."
            )
            learner_result = await create_learner(email=email, name=name, phone="")
            result["learner_response"] = learner_result
            result["learner_created"] = learner_result.get("success", False)

        if not learner_result.get("success"):
            logger.warning(
                f"Graphy learner creation returned non-success for {email}: "
                f"{learner_result.get('error')}. Attempting enrollment anyway (learner may already exist)."
            )

    assign_result = await assign_course(
        email=email,
        course_id=course_id,
        razorpay_payment_id=razorpay_payment_id,
        phone=phone,
        country_code=country_code,
    )
    result["assign_response"] = assign_result
    result["course_assigned"] = assign_result.get("success", False)

    if result["course_assigned"]:
        logger.info(f"Graphy enrollment complete for {email} in course {course_id}")
    else:
        logger.error(
            f"Graphy enrollment FAILED for {email} in course {course_id}: "
            f"{assign_result.get('error')}"
        )

    return result
