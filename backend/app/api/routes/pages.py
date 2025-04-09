from typing import Any
from fastapi import APIRouter, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageDraw
import tempfile
import os
import asyncio
from playwright.async_api import async_playwright
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

@router.get("/page3")
def read_page3(request : Request) -> Any:
    data = {
        "id": "002",
        "date": "19.11.2022",
        "apartment_number": "02",
        "building": "A1",
        "floor": "00",
        "apartment": "02"
    }
    return templates.TemplateResponse("page/page3.html", {"request": request, "data": data})

@router.get("/page4")
def read_page4(request : Request) -> Any:
    return templates.TemplateResponse("page/page4.html", {"request": request})

@router.get("/page5")
def read_page5(request : Request) -> Any:
    return templates.TemplateResponse("page/page5.html", {"request": request})

@router.get("/page6")
def read_page6(request : Request) -> Any:
    return templates.TemplateResponse("page/page6.html", {"request": request})

@router.get("/page7")
def read_page7(request : Request) -> Any:
    return templates.TemplateResponse("page/page7.html", {"request": request})

@router.get("/page8")
def read_page8(request : Request) -> Any:
    data = {
        'aptType' : 'A1'
    }
    return templates.TemplateResponse("page/page8.html", {"request": request , 'data': data})

@router.get("/page9")
def read_page9(request : Request) -> Any:
    data = {
        'aptType' : 'A1'
    }
    return templates.TemplateResponse("page/page9.html", {"request": request , 'data': data})

@router.get("/page10")
def read_page10(request : Request) -> Any:
    data = {
        'price' : 1000000
    }
    return templates.TemplateResponse("page/page10.html", {"request": request , 'data': data})

async def capture_page_pdfs(base_url: str, page_endpoints: list[str], output_dir: str) -> list[str]:
    """
    Capture PDFs of each page directly using Playwright.
    
    Args:
        base_url: The base URL of the application
        page_endpoints: List of page endpoints to capture
        output_dir: Directory to save the PDFs
        
    Returns:
        List of paths to the saved PDFs
    """
    pdf_paths = []
    
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)
        
        # Create a high-quality context
        context = await browser.new_context(
            viewport={"width": 1280, "height": 1696},  # Wide enough for A4
            device_scale_factor=2.0,  # Higher quality rendering
            is_mobile=False,
            has_touch=False,
            ignore_https_errors=True
        )
        
        # Enable console logging
        page = await context.new_page()
        page.on("console", lambda msg: print(f"BROWSER LOG: {msg.text}"))
        page.on("pageerror", lambda err: print(f"BROWSER ERROR: {err}"))
        
        for i, endpoint in enumerate(page_endpoints):
            try:
                full_url = f"{base_url.rstrip('/')}{endpoint}"
                print(f"Navigating to: {full_url}")
                
                # Navigate to the page with longer timeout
                response = await page.goto(full_url, wait_until="networkidle", timeout=30000)
                
                # Check if the navigation was successful
                if response.status >= 400:
                    print(f"Error loading page {endpoint}: HTTP {response.status}")
                    # Create a simple error PDF
                    pdf_path = os.path.join(output_dir, f"page_{i+1}_error.pdf")
                    # Use reportlab to create an error PDF
                    from reportlab.pdfgen import canvas
                    c = canvas.Canvas(pdf_path, pagesize=A4)
                    c.drawString(100, 500, f"Error loading page: HTTP {response.status}")
                    c.save()
                    pdf_paths.append(pdf_path)
                    continue
                
                # Wait a bit for any JavaScript to finish rendering
                await asyncio.sleep(2)
                
                # Optimize the page for PDF printing
                await page.evaluate("""() => {
                    document.body.style.width = '210mm';
                    document.body.style.height = '297mm';
                    document.body.style.margin = '0';
                    document.body.style.padding = '0';
                    document.documentElement.style.width = '210mm';
                    document.documentElement.style.height = '297mm';
                    document.documentElement.style.margin = '0';
                    document.documentElement.style.padding = '0';
                    
                    // Force all elements to properly fit
                    const allElements = document.querySelectorAll('*');
                    for (const el of allElements) {
                        if (el.style.position === 'fixed' || el.style.position === 'absolute') {
                            el.style.maxWidth = '210mm';
                        }
                    }
                    
                    // Set print-specific CSS
                    const style = document.createElement('style');
                    style.textContent = `
                        @media print {
                            body {
                                width: 210mm;
                                height: 297mm;
                                margin: 0;
                                padding: 0;
                            }
                            * {
                                page-break-inside: avoid;
                            }
                        }
                    `;
                    document.head.appendChild(style);
                }""")
                
                # Generate a PDF directly
                pdf_path = os.path.join(output_dir, f"page_{i+1}.pdf")
                await page.pdf(
                    path=pdf_path,
                    format="A4",
                    print_background=True,
                    prefer_css_page_size=True,
                    margin={"top": "0mm", "right": "0mm", "bottom": "0mm", "left": "0mm"},
                    scale=1.0  # No scaling
                )
                
                pdf_paths.append(pdf_path)
                print(f"PDF saved: {pdf_path}")
                
            except Exception as e:
                print(f"Error capturing {endpoint}: {str(e)}")
                # Create a simple error PDF
                pdf_path = os.path.join(output_dir, f"page_{i+1}_error.pdf")
                # Use reportlab to create an error PDF
                from reportlab.pdfgen import canvas
                c = canvas.Canvas(pdf_path, pagesize=A4)
                c.drawString(100, 500, f"Error: {str(e)}")
                c.save()
                pdf_paths.append(pdf_path)
        
        await browser.close()
    
    return pdf_paths

@router.get("/direct-pdf")
async def generate_direct_pdf(request: Request) -> Any:
    """
    Alternative endpoint that renders templates directly to PDFs.
    Uses in-memory rendering and Playwright to generate PDFs.
    """
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # List of functions and parameters to render each page
        page_renderers = [
            (read_pages, {}),
            (read_page2, {}),
            (read_page3, {}),
            (read_page4, {}),
            (read_page5, {}),
            (read_page6, {}),
            (read_page7, {}),
            (read_page8, {}),
            (read_page9, {}),
            (read_page10, {})
        ]
        
        # Generate HTML and PDFs for each page
        pdf_paths = []
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={"width": 1280, "height": 1696},
                device_scale_factor=2.0,
                ignore_https_errors=True
            )
            page = await context.new_page()
            
            for i, (renderer_func, params) in enumerate(page_renderers):
                try:
                    # Call the function that would normally render the template
                    response = renderer_func(request, **params)
                    
                    # If the response is a TemplateResponse, get the rendered HTML
                    if hasattr(response, "template") and hasattr(response, "context"):
                        # Render the template to HTML
                        rendered_html = templates.get_template(response.template.name).render(**response.context)
                        
                        # Add proper CSS for print
                        html_with_css = f"""
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <style>
                                @page {{
                                    size: A4;
                                    margin: 0;
                                }}
                                @media print {{
                                    body {{
                                        width: 210mm;
                                        height: 297mm;
                                        margin: 0;
                                        padding: 0;
                                    }}
                                }}
                                body {{
                                    width: 210mm;
                                    height: 297mm;
                                    margin: 0;
                                    padding: 0;
                                }}
                            </style>
                        </head>
                        <body>
                        {rendered_html}
                        </body>
                        </html>
                        """
                        
                        # Create a temporary HTML file
                        html_path = os.path.join(temp_dir, f"page_{i+1}.html")
                        with open(html_path, "w", encoding="utf-8") as f:
                            f.write(html_with_css)
                        
                        # Navigate to the file
                        await page.goto(f"file://{html_path}", wait_until="networkidle")
                        
                        # Wait for JavaScript rendering
                        await asyncio.sleep(1)
                        
                        # Optimize for PDF print
                        await page.evaluate("""() => {
                            document.body.style.width = '210mm';
                            document.body.style.height = '297mm';
                            document.body.style.margin = '0';
                            document.body.style.padding = '0';
                            document.documentElement.style.width = '210mm';
                            document.documentElement.style.height = '297mm';
                            document.documentElement.style.margin = '0';
                            document.documentElement.style.padding = '0';
                        }""")
                        
                        # Generate PDF
                        pdf_path = os.path.join(temp_dir, f"page_{i+1}.pdf")
                        await page.pdf(
                            path=pdf_path,
                            format="A4",
                            print_background=True,
                            prefer_css_page_size=True,
                            margin={"top": "0mm", "right": "0mm", "bottom": "0mm", "left": "0mm"},
                            scale=1.0
                        )
                        
                        pdf_paths.append(pdf_path)
                        print(f"PDF saved: {pdf_path}")
                    else:
                        print(f"Skipping page {i+1}: Not a template response")
                        
                except Exception as e:
                    print(f"Error rendering page {i+1}: {str(e)}")
                    # Create a simple error PDF
                    pdf_path = os.path.join(temp_dir, f"page_{i+1}_error.pdf")
                    from reportlab.pdfgen import canvas
                    c = canvas.Canvas(pdf_path, pagesize=A4)
                    c.drawString(100, 500, f"Error rendering page {i+1}")
                    c.drawString(100, 480, str(e))
                    c.save()
                    pdf_paths.append(pdf_path)
            
            await browser.close()
        
        # Combine all PDFs
        if pdf_paths:
            # Use PyPDF2 to merge PDFs
            from PyPDF2 import PdfMerger
            
            merger = PdfMerger()
            for pdf_path in pdf_paths:
                if os.path.exists(pdf_path):
                    merger.append(pdf_path)
            
            merged_path = os.path.join(temp_dir, "combined.pdf")
            merger.write(merged_path)
            merger.close()
            
            # Read the merged PDF
            with open(merged_path, "rb") as f:
                pdf_bytes = f.read()
            
            # Return the PDF as a streaming response
            return StreamingResponse(
                io.BytesIO(pdf_bytes),
                media_type="application/pdf",
                headers={"Content-Disposition": "attachment; filename=combined_pages.pdf"}
            )
        else:
            # Return an empty PDF if no pages were rendered
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=A4)
            c.drawString(100, 750, "No pages were rendered successfully")
            c.save()
            buffer.seek(0)
            return StreamingResponse(
                buffer,
                media_type="application/pdf",
                headers={"Content-Disposition": "attachment; filename=error.pdf"}
            )