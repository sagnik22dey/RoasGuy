from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from Routes import healthcheck
from Routes import homepage


app = FastAPI()

app.include_router(healthcheck.router)
app.include_router(homepage.router)


app.mount("/Resources", StaticFiles(directory="Resources"), name="Resources")


@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc):
    return JSONResponse(status_code=404, content={"message": "Page not found"})

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5500, reload=True)