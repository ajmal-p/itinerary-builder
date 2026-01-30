from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas import schemas
from app.crud import crud
import httpx
from datetime import datetime

router = APIRouter()


@router.post("/", response_model=schemas.Currency)
def create_currency(currency: schemas.CurrencyCreate, db: Session = Depends(get_db)):
    """Create a new currency"""
    # Check if code already exists
    existing = crud.crud_currency.get_by_code(db=db, code=currency.code.upper())
    if existing:
        raise HTTPException(status_code=400, detail="Currency code already exists")
    
    # If setting as base currency, unset others
    if currency.is_base_currency:
        base_curr = crud.crud_currency.get_base_currency(db=db)
        if base_curr:
            base_curr.is_base_currency = False
            db.add(base_curr)
            db.commit()
    
    return crud.crud_currency.create(db=db, obj_in=currency)


@router.get("/", response_model=List[schemas.Currency])
def list_currencies(
    skip: int = 0, 
    limit: int = 100, 
    active_only: bool = False,
    db: Session = Depends(get_db)
):
    """List all currencies"""
    if active_only:
        return crud.crud_currency.get_active_currencies(db=db)
    return crud.crud_currency.get_multi(db=db, skip=skip, limit=limit)


@router.get("/base", response_model=schemas.Currency)
def get_base_currency(db: Session = Depends(get_db)):
    """Get the base/library currency"""
    currency = crud.crud_currency.get_base_currency(db=db)
    if not currency:
        raise HTTPException(status_code=404, detail="No base currency configured")
    return currency


@router.get("/{currency_id}", response_model=schemas.Currency)
def get_currency(currency_id: int, db: Session = Depends(get_db)):
    """Get a specific currency"""
    currency = crud.crud_currency.get(db=db, id=currency_id)
    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found")
    return currency


@router.put("/{currency_id}", response_model=schemas.Currency)
def update_currency(
    currency_id: int, 
    currency: schemas.CurrencyUpdate, 
    db: Session = Depends(get_db)
):
    """Update a currency"""
    db_currency = crud.crud_currency.get(db=db, id=currency_id)
    if not db_currency:
        raise HTTPException(status_code=404, detail="Currency not found")
    
    # If setting as base currency, unset others
    if currency.is_base_currency:
        base_curr = crud.crud_currency.get_base_currency(db=db)
        if base_curr and base_curr.id != currency_id:
            base_curr.is_base_currency = False
            db.add(base_curr)
            db.commit()
    
    return crud.crud_currency.update(db=db, db_obj=db_currency, obj_in=currency)


@router.delete("/{currency_id}")
def delete_currency(currency_id: int, db: Session = Depends(get_db)):
    """Delete a currency"""
    currency = crud.crud_currency.get(db=db, id=currency_id)
    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found")
    
    if currency.is_base_currency:
        raise HTTPException(status_code=400, detail="Cannot delete base currency")
    
    crud.crud_currency.delete(db=db, id=currency_id)
    return {"message": "Currency deleted successfully"}


@router.post("/exchange-rates/", response_model=schemas.ExchangeRate)
def create_exchange_rate(
    exchange_rate: schemas.ExchangeRateCreate, 
    db: Session = Depends(get_db)
):
    """Create a new exchange rate"""
    return crud.crud_exchange_rate.create(db=db, obj_in=exchange_rate)


@router.get("/exchange-rates/", response_model=List[schemas.ExchangeRate])
def list_exchange_rates(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """List all exchange rates"""
    return crud.crud_exchange_rate.get_multi(db=db, skip=skip, limit=limit)


@router.get("/exchange-rates/latest", response_model=schemas.ExchangeRate)
def get_latest_exchange_rate(
    from_currency_id: int,
    to_currency_id: int,
    db: Session = Depends(get_db)
):
    """Get the latest exchange rate between two currencies"""
    rate = crud.crud_exchange_rate.get_latest_rate(
        db=db, 
        from_currency_id=from_currency_id, 
        to_currency_id=to_currency_id
    )
    if not rate:
        raise HTTPException(status_code=404, detail="Exchange rate not found")
    return rate


@router.post("/exchange-rates/fetch-from-api")
async def fetch_exchange_rates_from_api(
    base_currency_code: str = "USD",
    db: Session = Depends(get_db)
):
    """
    Fetch latest exchange rates from external API (exchangerate-api.com)
    This will update rates for all active currencies
    """
    base_currency = crud.crud_currency.get_by_code(db=db, code=base_currency_code.upper())
    if not base_currency:
        raise HTTPException(status_code=404, detail="Base currency not found")
    
    # Free API from exchangerate-api.com - replace with your preferred API
    api_url = f"https://api.exchangerate-api.com/v4/latest/{base_currency_code}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            response.raise_for_status()
            data = response.json()
        
        rates_updated = 0
        active_currencies = crud.crud_currency.get_active_currencies(db=db)
        effective_date = datetime.now()
        
        for currency in active_currencies:
            if currency.code in data.get("rates", {}):
                rate_value = data["rates"][currency.code]
                
                # Create new exchange rate record
                exchange_rate = schemas.ExchangeRateCreate(
                    from_currency_id=base_currency.id,
                    to_currency_id=currency.id,
                    rate=rate_value,
                    effective_date=effective_date,
                    source="exchangerate-api.com"
                )
                crud.crud_exchange_rate.create(db=db, obj_in=exchange_rate)
                rates_updated += 1
        
        return {
            "message": f"Successfully updated {rates_updated} exchange rates",
            "base_currency": base_currency_code,
            "effective_date": effective_date
        }
    
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=503, 
            detail=f"Failed to fetch exchange rates from API: {str(e)}"
        )
