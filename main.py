from fastapi import FastAPI, Response, Depends, Request
import uvicorn 
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from database import SessionLocal, Base, engine
from routers import user as router_user
from typing import Annotated

def lifespan(app):
    print('lifespan start')
    yield
    print('lifespan end')

Base.metadata.create_all(bind=engine)

app = FastAPI(title="my_project", summary="test", docs_url="/my_doc", lifespan=lifespan)

security = HTTPBearer()
@app.get("/secure-data")
def secure_data(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    return {"token": token}

app.include_router(router_user.router, prefix='/user')

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/it")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

@app.get("/set-cookie")
def set_cookie(response: Response):
    response.set_cookie(
        key="my_cookie", 
        value="cookie_value", 
        httponly=True, 
        max_age=3600,  
        expires=3600    
    )
    return {"message": "Cookie has been set"}

@app.get("/read-cookie")
def read_cookie(request: Request):
    my_cookie = request.cookies.get("my_cookie")
    if my_cookie:
        return {"cookie_value": my_cookie}
    else:
        return {"message": "No cookie found"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)