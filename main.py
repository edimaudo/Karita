"""Karita web application entry point."""

from pathlib import Path

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


APP_NAME = "Karita"
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".csv", ".xlsx"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB per file
MAX_FILES = 5

app = FastAPI(
    title=APP_NAME,
    description="Strategic decision support for nonprofit organizations.",
)

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the landing page."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": APP_NAME},
    )


@app.get("/reframer", response_class=HTMLResponse)
async def reframer(request: Request):
    """Render the problem reframing page."""
    return templates.TemplateResponse(
        request=request,
        name="reframer.html",
        context={"app_name": APP_NAME},
    )


@app.post("/reframer", response_class=HTMLResponse)
async def reframer_submit(
    request: Request,
    problem: str = Form(...),
    pillars: list[str] = Form(default=[]),
    assumptions: str = Form(default=""),
    attachments: list[UploadFile] = File(default=[]),
):
    """Receive the reframing form.

    The actual document processing and Nemotron workflow will be added later.
    For now, return the submitted inputs so the template contract is established.
    """
    problem = problem.strip()

    if len(attachments) > MAX_FILES:
        return templates.TemplateResponse(
            request=request,
            name="reframer.html",
            context={
                "app_name": APP_NAME,
                "error": f"Please upload no more than {MAX_FILES} files.",
                "problem": problem,
                "pillars": pillars,
                "assumptions": assumptions,
            },
            status_code=400,
        )

    uploaded_files = []

    for upload in attachments:
        if not upload.filename:
            continue

        extension = Path(upload.filename).suffix.lower()
        if extension not in ALLOWED_EXTENSIONS:
            return templates.TemplateResponse(
                request=request,
                name="reframer.html",
                context={
                    "app_name": APP_NAME,
                    "error": f"Unsupported file type: {upload.filename}",
                    "problem": problem,
                    "pillars": pillars,
                    "assumptions": assumptions,
                },
                status_code=400,
            )

        content = await upload.read(MAX_FILE_SIZE + 1)
        if len(content) > MAX_FILE_SIZE:
            return templates.TemplateResponse(
                request=request,
                name="reframer.html",
                context={
                    "app_name": APP_NAME,
                    "error": f"File exceeds the 10 MB limit: {upload.filename}",
                    "problem": problem,
                    "pillars": pillars,
                    "assumptions": assumptions,
                },
                status_code=400,
            )

        uploaded_files.append(
            {
                "filename": Path(upload.filename).name,
                "extension": extension,
                "size": len(content),
            }
        )

    return templates.TemplateResponse(
        request=request,
        name="reframer.html",
        context={
            "app_name": APP_NAME,
            "submitted": True,
            "problem": problem,
            "pillars": pillars,
            "assumptions": assumptions,
            "uploaded_files": uploaded_files,
            "reframed_problem": None,
        },
    )


@app.get("/solution-design", response_class=HTMLResponse)
async def solution_design(request: Request):
    """Render the solution design page."""
    return templates.TemplateResponse(
        request=request,
        name="solution_design.html",
        context={"app_name": APP_NAME},
    )


@app.post("/solution-design", response_class=HTMLResponse)
async def solution_design_submit(
    request: Request,
    problem: str = Form(default=""),
    reframed_problem: str = Form(default=""),
    pillars: list[str] = Form(default=[]),
    action: str = Form(default="generate"),
):
    """Receive the solution-design form.

    The consulting agents and Nemotron call will be connected here later.
    """
    return templates.TemplateResponse(
        request=request,
        name="solution_design.html",
        context={
            "app_name": APP_NAME,
            "problem": problem.strip(),
            "reframed_problem": reframed_problem.strip(),
            "pillars": pillars,
            "action": action,
            "solution": None,
        },
    )


@app.exception_handler(404)
async def not_found(request: Request, exc):
    """Render Karita's custom 404 page."""
    return templates.TemplateResponse(
        request=request,
        name="404.html",
        context={"app_name": APP_NAME},
        status_code=404,
    )
