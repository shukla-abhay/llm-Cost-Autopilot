from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.router.router import route
from app.router.classifier import predict

router = APIRouter()


class ChatRequest(BaseModel):
    prompt: str


class ChatResponse(BaseModel):
    response: str
    tier: str
    model: str
    complexity: str
    estimated_cost_usd: float
    input_tokens: int
    output_tokens: int


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    try:
        classification = predict(request.prompt)
        result = route(request.prompt)

        return ChatResponse(
            response=result.text,
            tier=result.tier,
            model=result.model_id,
            complexity=classification["complexity"],
            estimated_cost_usd=result.estimated_cost_usd,
            input_tokens=result.input_tokens,
            output_tokens=result.output_tokens,
        )
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Model unavailable: {str(e)}")
