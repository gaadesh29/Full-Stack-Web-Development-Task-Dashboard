from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.investment import Investment
from app.models.mutual_fund import MutualFund
from app.schemas.investment import InvestmentOut
from typing import List
from app.models.fund_sector_allocation import FundSectorAllocation
from app.models.sector import Sector
from app.models.fund_holding import FundHolding
from app.models.stock import Stock
from app.models.fund_marketcap_allocation import FundMarketCapAllocation
from sqlalchemy import func

router = APIRouter()

@router.get("/summary")
async def get_portfolio_summary():
    return {
        "current_value": 575000,
        "initial_value": 500000,
        "best_scheme": "ICICI Prudential Midcap Fund",
        "worst_scheme": "Axis Flexi Cap Fund"
    }

@router.get("/investment-overview", response_model=List[dict])
async def investment_overview(user_id: str = Query(...), db: AsyncSession = Depends(get_db)):
    # Query all investments for the user's portfolios
    result = await db.execute(
        select(Investment, MutualFund)
        .join(MutualFund, Investment.mutual_fund_id == MutualFund.id)
        .where(Investment.portfolio_id.in_(
            select(Investment.portfolio_id).where(Investment.portfolio_id == Investment.portfolio_id)
        ))
    )
    investments = result.all()
    overview = []
    for inv, mf in investments:
        overview.append({
            "mutual_fund": mf.name,
            "investment_date": inv.investment_date,
            "amount_invested": inv.amount_invested,
            "isin": mf.isin,
            "nav_at_investment": inv.nav_at_investment,
            "returns_since_investment": inv.returns_since_investment
        })
    return overview

@router.get("/sector-allocation")
async def sector_allocation(mutual_fund_id: str = Query(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(FundSectorAllocation, Sector)
        .join(Sector, FundSectorAllocation.sector_id == Sector.id)
        .where(FundSectorAllocation.mutual_fund_id == mutual_fund_id)
    )
    allocations = result.all()
    return [
        {"sector": sector.name, "weight_percent": fsa.weight_percent}
        for fsa, sector in allocations
    ]

@router.get("/stock-allocation")
async def stock_allocation(mutual_fund_id: str = Query(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(FundHolding, Stock)
        .join(Stock, FundHolding.stock_id == Stock.id)
        .where(FundHolding.mutual_fund_id == mutual_fund_id)
    )
    holdings = result.all()
    return [
        {"stock": stock.name, "symbol": stock.symbol, "weight_percent": fh.weight_percent}
        for fh, stock in holdings
    ]

@router.get("/marketcap-allocation")
async def marketcap_allocation(mutual_fund_id: str = Query(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(FundMarketCapAllocation)
        .where(FundMarketCapAllocation.mutual_fund_id == mutual_fund_id)
        .order_by(FundMarketCapAllocation.as_of_date.desc())
    )
    alloc = result.scalars().first()
    if not alloc:
        return {}
    return {
        "large_cap_percent": alloc.large_cap_percent,
        "mid_cap_percent": alloc.mid_cap_percent,
        "small_cap_percent": alloc.small_cap_percent
    }

@router.get("/overlap-analysis")
async def overlap_analysis(mutual_fund_ids: str = Query(...), db: AsyncSession = Depends(get_db)):
    # Parse mutual fund IDs
    fund_ids = [fid.strip() for fid in mutual_fund_ids.split(",") if fid.strip()]
    if len(fund_ids) < 2:
        raise HTTPException(status_code=400, detail="At least two mutual fund IDs are required.")

    # Query all holdings for these funds
    result = await db.execute(
        select(FundHolding, Stock, MutualFund)
        .join(Stock, FundHolding.stock_id == Stock.id)
        .join(MutualFund, FundHolding.mutual_fund_id == MutualFund.id)
        .where(FundHolding.mutual_fund_id.in_(fund_ids))
    )
    rows = result.all()

    # Group by stock
    stock_map = {}
    for fh, stock, mf in rows:
        key = (stock.id, stock.name, stock.symbol)
        if key not in stock_map:
            stock_map[key] = []
        stock_map[key].append({
            "mutual_fund": mf.name,
            "mutual_fund_id": str(mf.id),
            "weight_percent": fh.weight_percent
        })

    # Only include stocks present in more than one fund
    overlap = []
    for (stock_id, stock_name, stock_symbol), funds in stock_map.items():
        if len(funds) > 1:
            overlap.append({
                "stock": stock_name,
                "symbol": stock_symbol,
                "funds": funds
            })
    return overlap