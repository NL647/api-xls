import os
import time
from datetime import datetime
from time import sleep
import get_data
from fastapi import Depends, FastAPI, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security.api_key import APIKey
from fastapi.templating import Jinja2Templates
import auth
from fastapi.responses import JSONResponse
import uvicorn
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing_extensions import Annotated

FastAPI(docs_url=None, redoc_url=None)#desactive swagger
# auth
security = HTTPBasic()

# Get the date of creation of the SQLite database file


def get_database_creation_date():
    # Replace with your SQLite database file path
    sqlite_file = '/home/admin/api-xl/output.db'
    timestamp = os.path.getctime(sqlite_file)
    creation_date = datetime.fromtimestamp(timestamp)
    return creation_date


creation_date = get_database_creation_date()
print('days', creation_date)
current_date = datetime.now()
age = (current_date - creation_date).days
print('age:', age)

# Routes
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


def get_current_username(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    correct_username = "stanleybobson"
    correct_password = "swordfish"
    if (
        credentials.username != correct_username
        or credentials.password != correct_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db_age: int = age, username: str = Depends(get_current_username)):
    return templates.TemplateResponse("index.html", {"request": request, "db_age": db_age})

@app.get("/application", response_class=HTMLResponse)
def read_root(request: Request, db_age: int = age, username: str = Depends(get_current_username)):
    return templates.TemplateResponse("application.html", {"request": request, "db_age": db_age})

@app.get("/items/{server_id}", response_class=HTMLResponse)
async def read_item(
    request: Request, server_id: str, api_key: APIKey = Depends(auth.get_api_key), username: str = Depends(get_current_username)
):
    print("serverid", server_id)
    column_names, data_rows = get_data.get_data_by_hostname(server_id)

    if request.headers.get("accept") == "application/json":
        response_data = [column_names, data_rows]
        return JSONResponse(content=response_data)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "server_id": server_id,
            "column_names": column_names,
            "data_rows": data_rows,
            # "db_age": age
        },
    )
    
    
#by app name
@app.get("/applications/{application}", response_class=HTMLResponse)
async def read_applications(
    request: Request, application: str, api_key: APIKey = Depends(auth.get_api_key), username: str = Depends(get_current_username)
):
    column_names, data_rows = get_data.get_data_by_application(application)

    if request.headers.get("accept") == "application/json":
        response_data = [column_names, data_rows]
        return JSONResponse(content=response_data)

    return templates.TemplateResponse(
        "application.html",
        {
            "request": request,
            "application": application,
            "column_names": column_names,
            "data_rows": data_rows,
        },
    )

    

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=1,
        access_log=True,
        log_level='debug'
    )
