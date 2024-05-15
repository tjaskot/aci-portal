# Fast API Docs : https://fastapi.tiangolo.com/
# import uvicorn  # When using debugging, uncomment debug if statement at bottom of file.
import os
import ssl
import json
import secrets
import requests
import smtplib
from starlette.requests import Request as StarletteRequest  # To be used with Request.body forms
from fastapi import FastAPI, Request, HTTPException, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import Annotated
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


app = FastAPI(
    title="ACI Portal",
    description="ACI Portal POC",
    version="0.1"
)
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain('/etc/pki/nginx/server.crt', keyfile='/etc/pki/nginx/private/server.key')
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")
security = HTTPBasic()

invoice_list = [
    'Inv',
    'So#',
    'Date',
    'Warranty Start',
    'List',
    'Price',
    'Total'
]

mock_dict = {
    "customer_name": "John Doe",
    "orders": [
        {
            "order_number": "ORD123",
            "total": 100.5,
            "tax": 7.5,
            "shipping_cost": 10
        },
        {
            "order_number": "ORD124",
            "total": 75.25,
            "tax": 5.25,
            "shipping_cost": 8.5
        },
        {
            "order_number": "ORD125",
            "total": 200,
            "tax": 15,
            "shipping_cost": 12
        },
        {
            "order_number": "ORD126",
            "total": 50.75,
            "tax": 3.75,
            "shipping_cost": 5.5
        }
    ]
}


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


@app.get("/readData")
async def search(request: Request):
    """
    Description.
    :return:
    """
    url = "http://10.0.6.38:8080/db_test_call"
    headers = dict()
    auth = None
    db_dict = json.loads(requests.get(url=url, headers=headers, auth=auth).text)
    return templates.TemplateResponse("read_customer_data.html", {"request": request, "db_dict": db_dict})


@app.get("/changeCrm")
async def search(request: Request):
    """
    Description.
    :return:
    """
    return templates.TemplateResponse("change_crm.html", {"request": request})


@app.get("/invoices")
async def search(request: Request):
    """
    Description.
    :return:
    """
    # For mimetype, need to use requests package, not fastapi Request
    # TODO: get Request.body from form working in fastapi
    # r = requests.get("")
    # print(r)
    # # TODO: Mimetype e-mail
    # requestor = request.form['siteOwner']
    # # Change the string into list for concatenation later in function
    # recipient = [requestor]
    # cc = ['email@email.com']
    # bcc = []
    # sender = 'email@email.com'
    # msg = MIMEMultipart('alternative')
    # msg['Subject'] = 'Request Submitted'
    # msg['From'] = sender
    # msg['To'] = ",".join(recipient)
    # msg['CC'] = ",".join(cc)
    # msg['BCC'] = ",".join(bcc)
    # recipient += cc + bcc
    # # More detail in e-mail content
    # email_body = None
    # email_body_header = ' '
    # email_body_header += '<html><head></head><body>'
    # email_body_header += '<style type="text/css"></style>'
    # email_body_header += '<br><h2>Hello</h2><p>Email Header</p><br><p>Requested Info:</p><br>'
    # email_body_content = ' '
    # email_body_content += '<p> + requestor + </p>'
    # email_body_footer = ' '
    # email_body_footer += '<br>Thank you.'
    # email_body_footer += '<br><p>R/</p><p>Stalker Radar</p><br>'
    # html = str(email_body_header) + str(email_body_content) + str(email_body_footer)
    # part = MIMEText(html, 'html')
    # msg.attach(part)
    # s = smtplib.SMTP('mailhost.stalkerradar.com')
    # s.sendmail(sender, recipient, msg.as_string())
    # s.quit()
    return templates.TemplateResponse("list_pay_invoices.html",
                                      {"request": request, 'invoice_list': invoice_list})


@app.get("/contactUs")
async def search(request: Request):
    """
    Description.
    :return:
    """
    return templates.TemplateResponse("contact_us.html", {"request": request})


@app.get("/search")
async def search(request: Request):
    """
    Description.
    :return:
    """
    search_var = 'Search_variable'
    return templates.TemplateResponse("search.html", {"request": request, "search_var": search_var})


@app.post("/search")
async def search(search_param: str = Form(...)):
    """
    Description.
    :return:
    """
    return search_param


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
#     uvicorn.run(app, host="127.0.0.1", port=8000, ssl=ssl_context)
