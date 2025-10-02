from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from config.db import get_db
from crud.combined_tables import fetch_combined_leave_data

router = APIRouter(prefix="/combined", tags=["Combined Tables"])

@router.get("/all_leave_details")
async def all_leave_details(
    year: int = Query(...),
    month: int = Query(...),
    search: Optional[str] = "",
    limit: int = Query(10),
    offset: int = Query(0),
    db: AsyncSession = Depends(get_db)
):
    try:
        rows = await fetch_combined_leave_data(year, month, db)

        # Filter using search
        filtered = []
        for row in rows:
            if search and search.lower() not in str(row.employee_id).lower() and search.lower() not in row.employee_name.lower():
                continue
            filtered.append({
                "employee_id": row.employee_id,
                "employee_name": row.employee_name,
                "total_leaves": row.total_leaves_taken,
                "remaining_leaves": row.remaining_leaves,
                "leave_types": row.leave_types
            })

        total_count = len(filtered)
        paginated = filtered[offset:offset + limit]

        return {"data": paginated, "total": total_count}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
