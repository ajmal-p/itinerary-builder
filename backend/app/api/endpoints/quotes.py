from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas import schemas
from app.crud import crud
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.post("/", response_model=schemas.Quote)
def create_quote(quote: schemas.QuoteCreate, db: Session = Depends(get_db)):
    """Create a new quote"""
    # Verify enquiry exists
    enquiry = crud.crud_enquiry.get(db=db, id=quote.enquiry_id)
    if not enquiry:
        raise HTTPException(status_code=404, detail="Enquiry not found")
    
    # Verify itinerary exists
    itinerary = crud.crud_itinerary.get(db=db, id=quote.itinerary_id)
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    
    return crud.crud_quote.create_quote(db=db, obj_in=quote)


@router.get("/", response_model=List[schemas.Quote])
def list_quotes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all quotes"""
    return crud.crud_quote.get_multi(db=db, skip=skip, limit=limit)


@router.get("/{quote_id}", response_model=schemas.Quote)
def get_quote(quote_id: int, db: Session = Depends(get_db)):
    """Get a specific quote"""
    quote = crud.crud_quote.get(db=db, id=quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    return quote


@router.get("/enquiry/{enquiry_id}", response_model=List[schemas.Quote])
def get_enquiry_quotes(enquiry_id: int, db: Session = Depends(get_db)):
    """Get all quotes for an enquiry"""
    return crud.crud_quote.get_by_enquiry(db=db, enquiry_id=enquiry_id)


@router.put("/{quote_id}", response_model=schemas.Quote)
def update_quote(quote_id: int, quote: schemas.QuoteUpdate, db: Session = Depends(get_db)):
    """Update a quote"""
    db_quote = crud.crud_quote.get(db=db, id=quote_id)
    if not db_quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    
    # Recalculate total if markup changed
    if quote.markup_percentage is not None:
        total_price = db_quote.base_price * (1 + quote.markup_percentage / 100)
        db_quote.total_price = total_price
    
    return crud.crud_quote.update(db=db, db_obj=db_quote, obj_in=quote)


@router.delete("/{quote_id}")
def delete_quote(quote_id: int, db: Session = Depends(get_db)):
    """Delete a quote"""
    quote = crud.crud_quote.get(db=db, id=quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    crud.crud_quote.delete(db=db, id=quote_id)
    return {"message": "Quote deleted successfully"}


@router.get("/{quote_id}/pdf")
def export_quote_pdf(quote_id: int, db: Session = Depends(get_db)):
    """Export quote as PDF"""
    quote = crud.crud_quote.get(db=db, id=quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    
    # Get related data
    enquiry = crud.crud_enquiry.get(db=db, id=quote.enquiry_id)
    customer = crud.crud_customer.get(db=db, id=enquiry.customer_id)
    itinerary = crud.crud_itinerary.get(db=db, id=quote.itinerary_id)
    
    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph(f"Quote #{quote.id}", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Customer info
    customer_info = Paragraph(f"<b>Customer:</b> {customer.name}<br/><b>Email:</b> {customer.email}", styles['Normal'])
    elements.append(customer_info)
    elements.append(Spacer(1, 12))
    
    # Itinerary info
    itinerary_info = Paragraph(f"<b>Itinerary:</b> {itinerary.name}<br/><b>Description:</b> {itinerary.description or 'N/A'}", styles['Normal'])
    elements.append(itinerary_info)
    elements.append(Spacer(1, 12))
    
    # Pricing table
    pricing_data = [
        ['Description', 'Amount'],
        ['Base Price', f'${quote.base_price:.2f}'],
        ['Markup', f'{quote.markup_percentage}%'],
        ['Total Price', f'${quote.total_price:.2f}']
    ]
    
    table = Table(pricing_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=quote_{quote.id}.pdf"}
    )
