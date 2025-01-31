import os
import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from core.settings import settings

from api_v1 import router as router_v1


app = FastAPI()

app.include_router(router=router_v1, prefix=settings.api_v1_prefix)
app.mount(
    settings.avatar_url,
    StaticFiles(directory=settings.avatar_directory),
    name="avatars",
)


@app.get("/")
async def start_test():
    return {"message": "1, 2, 3 Start! Service Auth V2!"}


if __name__ == "__main__":
    os.makedirs(
        settings.avatar_directory, exist_ok=True
    )  # Убедитесь, что директория существует
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload_serv,
    )
