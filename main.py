from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
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

@app.get("/solution-design", response_class=HTMLResponse)
async def read_solution_design(request: Request):
    return templates.TemplateResponse("solution_design.html", {"request": request})

@app.exception_handler(404)
async def custom_404_handler(request, __):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

# # Simple explicit password string definition for verification
# ADMIN_SECRET_KEY = "KaritaGTA2026"

# # Mock internal memory database store to represent the Qwen database records
# # When user triggers "Save" in solution_design.html, it posts data here
# MOCK_QWEN_DATABASE = [
#     {
#         "name": "Edima Pascal",
#         "email": "epascal@gtacommunity.org",
#         "city": "Toronto",
#         "postal": "M5V 2L7",
#         "province": "Ontario",
#         "problem": "[CORE CHALLENGE]\nVolunteer retention has collapsed by 40% post-pandemic, driving up operational overhead costs.\n\n[KEY VARIABLES]\nLimited manual training workflows, low engagement metrics.",
#         "solution": "1. Deploy an Automated Engagement Track using clear operational templates.\n2. Leverage targeted cost optimization structures within regional centers.",
#         "agents_used": ["reframer-agent", "operations-agent", "financial-agent"]
#     }
# ]

# @app.get("/review", response_class=HTMLResponse)
# async def get_review_portal(request: Request, logout: bool = False):
#     if logout:
#         response = templates.TemplateResponse("review.html", {"request": request, "authenticated": False})
#         response.delete_cookie(key="auth_token")
#         return response

#     # Check for authorization tracking token cookie
#     auth_cookie = request.cookies.get("auth_token")
#     authenticated = (auth_cookie == "authorized_session_established")
    
#     return templates.TemplateResponse("review.html", {
#         "request": request, 
#         "authenticated": authenticated,
#         "records": MOCK_QWEN_DATABASE
#     })

# @app.post("/review", response_class=HTMLResponse)
# async def post_review_login(request: Request, password: str = Form(...)):
#     if password == ADMIN_SECRET_KEY:
#         response = RedirectResponse(url="/review", status_code=303)
#         response.set_cookie(key="auth_token", value="authorized_session_established", httponly=True)
#         return response
    
#     return templates.TemplateResponse("review.html", {
#         "request": request, 
#         "authenticated": False, 
#         "error": "Invalid administrator access credentials. Please try again."
#     })
