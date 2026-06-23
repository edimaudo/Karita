from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI(title="Karita")

# In production on Vercel, static files can be served directly, but this is good for local dev.
# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def read_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/reframer", response_class=HTMLResponse)
async def read_reframer(request: Request):
    return templates.TemplateResponse("reframer.html", {"request": request})

@app.get("/solution-design", response_class=HTMLResponse)
async def read_solution_design(request: Request):
    return templates.TemplateResponse("solution_design.html", {"request": request})

# API Endpoint for the Reframer Agent
@app.post("/reframe")
async def process_reframe(request: Request):
    data = await request.json()
    service = data.get("service")
    sub_service = data.get("sub_service")
    problem = data.get("problem")
    
    # TODO: Integrate Qwen Reframer Agent logic here
    # Mock response for scaffolding
    reframed_output = f"Through the lens of {service} ({sub_service}), the core challenge is structured as follows: {problem}"
    
    return JSONResponse({"success": True, "framedProblem": reframed_output})

@app.exception_handler(404)
async def custom_404_handler(request, __):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
