import json
import logging
import sys
import threading
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

app = FastAPI(title="Key-Value Storage Server")

DATABASE_URL = "sqlite:///./storage.db"
JSON_FILE = Path(__file__).parent / "data.json"
LOG_FILE = Path(__file__).parent / "app.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("kv-storage")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

file_lock = threading.Lock()

class KeyValueModel(Base):
    __tablename__ = "key_values"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    value = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup_event():
    logger.info("=" * 60)
    logger.info("Application startup initiated")
    logger.info(f"Database: {DATABASE_URL}")
    logger.info(f"JSON Storage: {JSON_FILE}")
    logger.info(f"Log File: {LOG_FILE}")
    logger.info("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("=" * 60)
    logger.info("Application shutdown initiated")
    logger.info("=" * 60)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = f"{int(time.time() * 1000)}"
    start_time = time.time()
    
    logger.info(
        f"[{request_id}] --> {request.method} {request.url.path}",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "client_ip": request.client.host if request.client else "unknown",
        }
    )
    
    try:
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        
        logger.info(
            f"[{request_id}] <-- {request.method} {request.url.path} "
            f"status={response.status_code} duration={process_time:.2f}ms",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": f"{process_time:.2f}",
            }
        )
        
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
        return response
        
    except Exception as exc:
        process_time = (time.time() - start_time) * 1000
        logger.error(
            f"[{request_id}] !!! {request.method} {request.url.path} "
            f"error={str(exc)} duration={process_time:.2f}ms",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "error": str(exc),
                "duration_ms": f"{process_time:.2f}",
                "traceback": traceback.format_exc(),
            }
        )
        raise

class WriteRequest(BaseModel):
    key: str
    value: str

class ReadRequest(BaseModel):
    key: str

class ValueResponse(BaseModel):
    key: str
    value: str

def read_json_file() -> dict:
    if not JSON_FILE.exists():
        return {}
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def write_json_file(data: dict) -> None:
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.post("/write")
def write_key_value(request: WriteRequest):
    logger.info(
        f"Write operation initiated: key='{request.key}' "
        f"value_length={len(request.value)}"
    )
    
    db = SessionLocal()
    try:
        existing = db.query(KeyValueModel).filter(KeyValueModel.key == request.key).first()
        
        if existing:
            logger.info(f"Updating existing key: '{request.key}'")
            existing.value = request.value
            operation = "UPDATE"
        else:
            logger.info(f"Creating new key: '{request.key}'")
            db_obj = KeyValueModel(key=request.key, value=request.value)
            db.add(db_obj)
            operation = "CREATE"
        
        db.commit()
        logger.info(f"Database commit successful: operation={operation} key='{request.key}'")
        
        with file_lock:
            data = read_json_file()
            data[request.key] = request.value
            write_json_file(data)
            logger.info(f"JSON file updated: key='{request.key}'")
        
        logger.info(f"Write operation completed: key='{request.key}' status=success")
        return {"status": "success", "message": f"Key '{request.key}' saved successfully"}
    except Exception as e:
        logger.error(
            f"Write operation failed: key='{request.key}' error='{str(e)}' "
            f"traceback={traceback.format_exc()}"
        )
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.post("/read")
def read_key_value(request: ReadRequest):
    logger.info(f"Read operation initiated: key='{request.key}'")
    
    try:
        with file_lock:
            data = read_json_file()
        
        value = data.get(request.key)
        
        if value is None:
            logger.warning(f"Read operation - key not found: '{request.key}'")
            raise HTTPException(status_code=404, detail=f"Key '{request.key}' not found")
        
        logger.info(
            f"Read operation completed: key='{request.key}' "
            f"value_length={len(str(value))} status=success"
        )
        return {"key": request.key, "value": value}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Read operation failed: key='{request.key}' error='{str(e)}' "
            f"traceback={traceback.format_exc()}"
        )
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    import argparse
    
    parser = argparse.ArgumentParser(description="Key-Value Storage Server")
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=7890,
        help="Server port (default: 7890)"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Server host (default: 0.0.0.0)"
    )
    args = parser.parse_args()
    
    logger.info("Starting Key-Value Storage Server...")
    logger.info(f"Server will listen on http://{args.host}:{args.port}")
    logger.info(f"API documentation available at http://localhost:{args.port}/docs")
    logger.info("=" * 60)
    
    uvicorn.run(app, host=args.host, port=args.port)
