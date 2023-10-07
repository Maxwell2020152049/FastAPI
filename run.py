"""
主程序
"""

import uvicorn
from fastapi import FastAPI
from user import app_user

app = FastAPI()

app.include_router(app_user, prefix="/user", tags=["user"])

if __name__ == "__main__":
    uvicorn.run('run:app', host='0.0.0.0', port=8000, reload=True, workers=4)
