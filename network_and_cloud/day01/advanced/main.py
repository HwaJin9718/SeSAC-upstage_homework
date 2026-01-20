import sys
import json
import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request
import uvicorn
from network_and_cloud.day01.advanced.controller import todo_route
from loguru import logger

app = FastAPI()
app.include_router(todo_route.todo_route)

logger.remove()

# 콘솔 출력 설정 (형식 지정)
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO"
)

# ---------------------------
# Request/Response 로깅 미들웨어 (수정 버전)
# ---------------------------
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 시작 시간 기록
        start_time = time.time()
        
        # ========== Request Body 로깅 ==========
        logger.info("=" * 60)
        logger.info("📥 INCOMING REQUEST")
        logger.info("=" * 60)
        
        # HTTP Method와 URL
        logger.info(f"Method: {request.method}")
        logger.info(f"URL: {request.url}")
        logger.info(f"Path: {request.url.path}")
        
        # Query Parameters
        if request.query_params:
            logger.info(f"Query Parameters: {dict(request.query_params)}")
        
        # 주요 헤더 출력
        logger.info("Headers:")
        important_headers = ["host", "user-agent", "content-type", "authorization", "accept"]
        for header in important_headers:
            if header in request.headers:
                # Authorization은 보안을 위해 마스킹
                if header == "authorization":
                    logger.info(f"  - {header.capitalize()}: {'*' * 10}")
                else:
                    logger.info(f"  - {header.capitalize()}: {request.headers[header]}")
        
        # Request Body 로깅 (수정된 부분)
        body_bytes = await request.body()
        if body_bytes:
            try:
                body_json = json.loads(body_bytes.decode())
                logger.info(f"Body: {json.dumps(body_json, indent=2, ensure_ascii=False)}")
            except:
                logger.info(f"Body (raw): {body_bytes.decode()[:200]}")  # 처음 200자만
        
        # 실제 엔드포인트 실행
        response = await call_next(request)
        
        # 처리 시간 계산
        process_time = time.time() - start_time
        
        # ========== Response Body 로깅 ==========
        logger.info("-" * 60)
        logger.info("📤 OUTGOING RESPONSE")
        logger.info("-" * 60)
        
        # 응답 상태 코드
        logger.info(f"Status Code: {response.status_code}")
        
        # 주요 응답 헤더 출력
        logger.info("Response Headers:")
        response_headers = ["content-type", "content-length"]
        for header in response_headers:
            if header in response.headers:
                logger.info(f"  - {header.capitalize()}: {response.headers[header]}")
        
        # 처리 시간
        logger.info(f"Processing Time: {process_time:.4f}s")
        logger.info("=" * 60)
        logger.info("")
        
        return response

# 미들웨어 등록
app.add_middleware(LoggingMiddleware)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)