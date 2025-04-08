from typing import Any

from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates

from app.api.deps import CurrentUser, SessionDep

router = APIRouter(prefix="/pages", tags=["pages"])

templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def read_pages(request : Request) -> Any:
    data = {
        "id": "1"+ " : " + "العدد",
        "buildng": "A1"+ " | " + "العمارة",
        "floor": "00"+ " | " + "الطابق",
        "apartment": "02"+ " | " + "الشقة"
    }
    return templates.TemplateResponse("page/page1.html", {"request": request, "data": data})

@router.get("/page2")
def read_page2(request : Request) -> Any:
    data = {
        "date": "19.11.2022",
        "id": "002",
        "customer_name": "محمد علي علي",
        "unified_card_number": "1234567890",
        "id_number": "1234567890",
        "registry_number": "1234567890",
        "newspaper_number": "1234567890",
        "issue_date": "19.11.2022",
        "district": "محلة",
        "street": "زقاق",
        "house": "دار",
        "alt_district": "محلة",
        "alt_street": "زقاق",
        "alt_house": "دار",
        "phone_number": "01234567890",
        "job_title": "وظيفة",
        "alt_person_name": "محمد علي علي",
        "relationship": "والد",
        "alt_person_number": "1234567890"
    }
    return templates.TemplateResponse("page/page2.html", {"request": request, "data": data})