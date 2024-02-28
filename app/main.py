# Fast API Docs : https://fastapi.tiangolo.com/
# import uvicorn  # When using debugging, uncomment debug if statement at bottom of file.
import secrets
from fastapi import FastAPI, Request, HTTPException, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import dotenv_values, load_dotenv
from pathlib import Path
from typing import Annotated


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

security = HTTPBasic()
templates = Jinja2Templates(directory="templates")

# get config values from .env
config = dotenv_values(".env")
dotenv_path = Path('path/to/.env')
load_dotenv(dotenv_path=dotenv_path)


def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"stan"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"fish"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/")
async def root(request: Request):
    """
    Description.
    :return:
    """
    return RedirectResponse(url="/login")


@app.get("/users/admin")
def read_current_user(username: Annotated[str, Depends(get_current_username)]):
    """
    Description.
    :return:
    """
    return {"username": username}


# Request details from Starlette: https://www.starlette.io/requests/
@app.api_route("/login", methods=["GET", "POST"])
async def login(request: Request):
    """
    Description.
    :return:
    """
    if request.method == "POST":
        # print(request.method)
        # async with request.form() as form:
        #     print(form.get("userEmail"))
        return templates.TemplateResponse("login_success.html", {"request": request})
    elif request.method == "GET":
        customer_name = "john doe"
        return templates.TemplateResponse("login.html", {"request": request,
                                                         "customer_name": customer_name})
    else:
        return "Method not allowed"


@app.get("/index", response_class=HTMLResponse)
async def home(request: Request):
    """
    Description.
    :return:
    """
    if request.method.lower() != 'get':
        # Raise http exceptions for unsupported request methods, Json responses for data handling
        raise HTTPException(
            status_code=405,
            detail=f"Request method not allowed: {request.method}"
        )
    else:
        index_var = 'Index_variable'
        return templates.TemplateResponse("index.html", {"request": request, "index_var": index_var})


@app.get("/search")
async def search(request: Request):
    """
    Description.
    :return:
    """
    search_var = 'Search_variable'
    return templates.TemplateResponse("search.html", {"request": request, "search_var": search_var})


@app.get("/api")
async def default(request: Request):
    """
    Description.
    :return:
    """
    return JSONResponse(
        content={
            "Info": "Below these are the endpoints that are reserved for our application with a brief description",
            "/": "Root page for SSO",
            "index": "Index Url - html response",
            "search": "Second browser endpoint - html response",
            "keepalive": "Keepalive 200 response",
            "api": "List of api endpoints, both browser and json api responses - Json Response",
            "docs": "Swagger API docs"
        },
        status_code=200
    )


@app.get("/keepalive")
async def keepalive():
    """
    Description.
    :return:
    """
    return {
        "keepalive":
            200
    }


# Used for debugging purposes
#   Uncomment 'import uvicorn' at top of file
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
