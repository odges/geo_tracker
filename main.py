from fastapi import FastAPI, Response
import uvicorn
from schemas.geo import UserGeo

app = FastAPI()


@app.post("/geo")
def recive_user_geo(user_geo: UserGeo):
    """Получение geo данных"""
    return Response(status_code=200)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
