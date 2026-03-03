from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from httpx import request

from routes.student_route import router as student_router
from routes.address_route import router as address_router
from routes.phone_route import router as phone_router
from routes.email_routes import router as email_router

app = FastAPI(title= "TCA Project API", version="1.0.0", description="API for TCA Project")


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

api_route = "/api/v1"

app.include_router(student_router, prefix=api_route, tags=["Students"])
app.include_router(address_router, prefix=api_route, tags=["Addresses"])
app.include_router(phone_router, prefix=api_route, tags=["Phones"])
app.include_router(email_router, prefix=api_route, tags=["Emails"])

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/students/{student_id}/view")
async def student_detail_view(student_id: int, request: Request):
    return templates.TemplateResponse(
        "student-detail.html",
        {"request": request, "student_id": student_id}
    )

@app.get(f"{api_route}/health")
def health_check():
    return {"status": "healthy"}