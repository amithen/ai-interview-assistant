from fastapi import File,UploadFile,HTTPException,APIRouter
from app.services.llm_service import analyze_resume
from pypdf import PdfReader
import io
router = APIRouter(
    prefix="/resume",
    tags=["resume"],
)

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400,detail="Only PDF files are allowed")

    content = await file.read()

    pdf_reader = PdfReader(io.BytesIO(content))

    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""

    ai_response = analyze_resume(text)

    return {"file":file.filename,
            "size":len(content),
            "ai_response":ai_response}

