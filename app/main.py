# Fast API Docs : https://fastapi.tiangolo.com/
# import uvicorn  # When using debugging, uncomment debug if statement at bottom of file.
import os
import ssl
import json
import secrets
import requests
from fastapi import FastAPI, Request, HTTPException, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

app = FastAPI(
    title="ACI Portal",
    description="ACI Portal POC",
    version="1.5"
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
    with open(os.path.join(os.getcwd(), "app", "common", "resources", "customer_info.json"), "r") as cust_json:
        customer_info = json.load(cust_json)
    return templates.TemplateResponse("read_customer_data.html", {
        "request": request,
        "db_dict": db_dict,
        "customer_info": customer_info
    })


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
async def contact_us(request: Request):
    """
    Description.
    :return:
    """
    render_dict = dict()
    cwd = os.getcwd()
    dropdown_file = "dropdown.json"
    with open(os.path.join(cwd, "app", "common", "resources", dropdown_file), "r") as dropdown_json:
        render_dict = json.load(dropdown_json)
    return templates.TemplateResponse("contact_us.html", {"request": request, "render_dict": render_dict})


@app.post("/contactUs")
async def contact_us(firstname: str = Form(...), lastname: str = Form(...),
                     options: str = Form(...),
                     rank: str = Form(...),
                     department: str = Form(...),
                     zipcode: str = Form(...),
                     stateOption: str = Form(...),
                     phoneNumber: str = Form(...),
                     email: str = Form(...),
                     contactOption: str = Form(...),
                     message: str = Form(...),
                     emailCommunication: str = Form(...),
                     mailCommunication: str = Form(...),
                     telephoneCommunication: str = Form(...),
                     textCommunication: str = Form(...)):
    """
    Handle the form submission.
    :return: First and last name
    """
    form_data = {"firstName": firstname,
            "lastName": lastname,
            "rank": rank,
            "options": options,
            "department": department,
            "zipcode": zipcode,
            "stateOption": stateOption,
            "phoneNumber": phoneNumber,
            "email": email,
            "contactOption": contactOption,
            "message": message,
            "emailCommunication": emailCommunication,
            "mailCommunication": mailCommunication,
            "telephoneCommunication": telephoneCommunication,
            "textCommunication": textCommunication
            }
    path = os.getcwd()
    with open("my_created_file.txt", "w") as test_file:
        test_file.write(str(form_data))
    return form_data


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


@app.get("/page_render")
async def page_render(request: Request):
    """
    Description.
    :return:
    """
    # render_list = ["Alabama", "Alaska", "Arizona", "Arkansas", "Armed Forces Americas", "Armed Forces Europe",
    #                "Armed Forces Pacific", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia",
    #                "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
    #                "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri",
    #                "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York",
    #                "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island",
    #                "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    #                "West Virginia", "Wisconsin", "Wyoming"]
    cwd = os.getcwd()
    dropdown_file = "dropdown.json"
    with open(os.path.join(cwd, "app", "common", "resources", dropdown_file), "r") as dropdown_json:
        render_dict = json.load(dropdown_json)
    return templates.TemplateResponse("render_html.html", {"request": request, "render_dict": render_dict})


@app.post("/page_render")
async def page_render(state_dropdown: str = Form(...)):
    """
    Description.
    :return:
    """
    render_dict = {"Alabama": "AL", "Alaska": "AK"}
    dropdown_value = render_dict[state_dropdown]
    return {"dropdown_value": dropdown_value}


@app.api_route("/qm_json", methods=["GET", "POST"])
async def qm_json(request: Request):
    """
    Call QM database and have return response with passed json parameters
    :return:
    """
    if request.method == "GET":
        customer_details = str()
        return templates.TemplateResponse("qm_json_call.html", {"request": request,
                                                                "customer_details": customer_details})
    if request.method == "POST":
        # mcode = customer_number
        form_data = await request.form()
        mcode = form_data["customer_number"]
        url = "http://10.0.6.38:5000/qm_json"

        payload = json.dumps({
            "Token": "U2FsdGVkX1%2BE1aKFQHHkJJSpgryqlmld3lPblvPH8BI%3D",
            "UID": "connor",
            "mcode": "750861",
            "action": "onload.address",
            "program_name": "CSD.HOME.SUBS",
            "sessionid": "1718305604831715626-20619-50804"
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response_json = json.loads(response.text)
        # return response_json
        return templates.TemplateResponse("qm_json_call.html", {"request": request, "customer_details": response_json})

"""
--- IMPORTANT NOTES ---
1. APIs below this line should not be moved and used for application monitoring end-points.
2. New end-points can be added but application relevant routes should all be above this line.
"""


@app.get("/api")
async def default(request: Request):
    """
    Overview list of basic API's available.
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
    Keep Alive endpoint leveraged for dashboards and telemetry of 200 status.
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
