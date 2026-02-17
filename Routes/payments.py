from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import razorpay
import hmac
import hashlib
import os
import logging
from dotenv import load_dotenv
from services.graphy import create_and_enroll_learner

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")
TEST_PRICE_OVERRIDE = os.getenv("TEST_PRICE_OVERRIDE")

logger.info(f"Razorpay Key ID loaded: {RAZORPAY_KEY_ID[:10]}..." if RAZORPAY_KEY_ID else "Razorpay Key ID NOT loaded")
logger.info(f"Razorpay Key Secret loaded: {'Yes' if RAZORPAY_KEY_SECRET else 'No'}")
if TEST_PRICE_OVERRIDE:
    logger.warning(f"TEST_PRICE_OVERRIDE is active: all Razorpay orders will be charged {TEST_PRICE_OVERRIDE} paise")

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


COURSE_PRICES = {
    "fundamentals-of-facebook-ads": {
        "name": "Fundamentals of Facebook Ads",
        "amount": 99900,
        "currency": "INR",
        "price_env": "PRICE_FUNDAMENTALS"
    },
    "basic-plan": {
        "name": "Basic Plan",
        "amount": 1399100,
        "currency": "INR",
        "price_env": "PRICE_BASIC_PLAN"
    },
    "business-growth-plan": {
        "name": "Business Growth Plan",
        "amount": 4999100,
        "currency": "INR",
        "price_env": "PRICE_BUSINESS_GROWTH"
    },
    "value-plan": {
        "name": "Value Plan",
        "amount": 1499100,
        "currency": "INR",
        "price_env": "PRICE_VALUE_PLAN"
    },
    "master-creative-targeting-base": {
        "name": "Master Creative Targeting - Base Plan",
        "amount": 199100,
        "currency": "INR",
        "price_env": "PRICE_MCT_BASE"
    },
    "master-creative-targeting-mentorship": {
        "name": "Master Creative Targeting - Mentorship Plan",
        "amount": 499100,
        "currency": "INR",
        "price_env": "PRICE_MCT_MENTORSHIP"
    }
}

for cid, cdata in COURSE_PRICES.items():
    env_val = os.getenv(cdata["price_env"])
    if env_val:
        logger.warning(f"Price override active for '{cid}': {env_val} paise (env: {cdata['price_env']})")


class CreateOrderRequest(BaseModel):
    course_id: str
    name: str
    email: str
    phone: str


class VerifyPaymentRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    course_id: str
    name: str
    email: str
    phone: str


@router.post("/api/create-order")
async def create_order(request: CreateOrderRequest):
    """
    Create a Razorpay order for the specified course.
    """
    logger.info(f"Creating order for course: {request.course_id}")
    logger.info(f"Customer: {request.name}, Email: {request.email}, Phone: {request.phone}")
    
    course = COURSE_PRICES.get(request.course_id)
    
    if not course:
        logger.error(f"Invalid course ID: {request.course_id}")
        raise HTTPException(status_code=400, detail="Invalid course ID")
    
    try:
        import time
        receipt_id = f"rcpt_{int(time.time())}"
        
        env_override = os.getenv(course["price_env"])
        charge_amount = int(env_override) if env_override else course["amount"]
        
        order_data = {
            "amount": charge_amount,
            "currency": course["currency"],
            "receipt": receipt_id,
            "notes": {
                "course_id": request.course_id,
                "course_name": course["name"],
                "customer_name": request.name,
                "customer_email": request.email,
                "customer_phone": request.phone
            }
        }
        
        logger.info(f"Order data: {order_data}")
        order = client.order.create(data=order_data)
        logger.info(f"Order created successfully: {order['id']}")
        
        return JSONResponse(content={
            "success": True,
            "order_id": order["id"],
            "amount": charge_amount,
            "currency": course["currency"],
            "key_id": RAZORPAY_KEY_ID,
            "course_name": course["name"],
            "prefill": {
                "name": request.name,
                "email": request.email,
                "contact": request.phone
            }
        })
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


async def _enroll_on_graphy(email: str, name: str, phone: str, course_id: str, razorpay_payment_id: str):
    """
    Background task: Create learner on Graphy and enroll them in the purchased course.
    Runs after the payment verification response is sent to the user.
    """
    try:
        result = await create_and_enroll_learner(
            email=email,
            name=name,
            phone=phone,
            course_id=course_id,
            razorpay_payment_id=razorpay_payment_id,
        )
        if result["course_assigned"]:
            logger.info(f"Graphy enrollment SUCCESS for {email} | course: {course_id} | payment: {razorpay_payment_id}")
        else:
            logger.error(f"Graphy enrollment FAILED for {email} | course: {course_id} | details: {result}")
    except Exception as e:
        logger.error(f"Graphy enrollment background task error for {email}: {str(e)}")


@router.post("/api/verify-payment")
async def verify_payment(request: VerifyPaymentRequest, background_tasks: BackgroundTasks):
    """
    Verify the Razorpay payment signature, confirm the payment,
    and trigger Graphy learner creation + course enrollment in the background.
    """
    try:
        message = f"{request.razorpay_order_id}|{request.razorpay_payment_id}"
        generated_signature = hmac.new(
            RAZORPAY_KEY_SECRET.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        
        if generated_signature != request.razorpay_signature:
            raise HTTPException(status_code=400, detail="Invalid payment signature")
        
        background_tasks.add_task(
            _enroll_on_graphy,
            email=request.email,
            name=request.name,
            phone=request.phone,
            course_id=request.course_id,
            razorpay_payment_id=request.razorpay_payment_id,
        )
        
        return JSONResponse(content={
            "success": True,
            "message": "Payment verified successfully",
            "payment_id": request.razorpay_payment_id,
            "order_id": request.razorpay_order_id
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/razorpay-key")
async def get_razorpay_key():
    """
    Return the Razorpay public key ID for frontend use.
    """
    return JSONResponse(content={
        "key_id": RAZORPAY_KEY_ID
    })
