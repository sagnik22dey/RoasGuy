import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from dotenv import load_dotenv

load_dotenv()

from Routes import healthcheck
from Routes import homepage
from Routes import thankYouPage
from Routes import cartpage
from Routes import advancedHomepage
from Routes import metaHomepage
from Routes import policyPages
from Routes import payments
app = FastAPI()

@app.get("/.well-known/appspecific/com.chrome.devtools.json")
async def chrome_devtools_config():
    return {}

app.include_router(healthcheck.router)
app.include_router(homepage.router)
app.include_router(thankYouPage.router)
app.include_router(cartpage.router)
app.include_router(advancedHomepage.router)
app.include_router(metaHomepage.router)
app.include_router(policyPages.router)
app.include_router(payments.router)

app.mount("/Resources", StaticFiles(directory="Resources"), name="Resources")
app.mount("/style", StaticFiles(directory="style"), name="style")



@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc):
    return JSONResponse(status_code=404, content={"message": "Page not found"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5500))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)