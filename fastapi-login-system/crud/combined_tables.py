from sqlalchemy import select, func, extract, and_, String
from sqlalchemy.ext.asyncio import AsyncSession
from models import User, LeaveApplications, LeaveTypes, LeaveDetails, RemainingLeaves

async def fetch_combined_leave_data(year: int, month: int, db: AsyncSession):
    # Leave type breakdown (e.g. sick:6, casual:4)
    leave_type_breakdown = (
        select(
            LeaveApplications.employee_id,
            LeaveTypes.leave_type.label("leave_type"),
            func.sum(LeaveApplications.total_days).label("days_taken")
        )
        .join(LeaveTypes, LeaveApplications.leave_type_id == LeaveTypes.id)
        .where(
            and_(
                extract("year", LeaveApplications.start_date) == year,
                extract("month", LeaveApplications.start_date) == month,
                LeaveApplications.status == "approved"
            )
        )
        .group_by(LeaveApplications.employee_id, LeaveTypes.leave_type)
        .subquery()
    )

    # Total approved leaves taken this month
    total_leaves_taken_sub = (
        select(
            LeaveApplications.employee_id,
            func.sum(LeaveApplications.total_days).label("total_leaves_taken")
        )
        .where(
            and_(
                extract("year", LeaveApplications.start_date) == year,
                extract("month", LeaveApplications.start_date) == month,
                LeaveApplications.status == "approved"
            )
        )
        .group_by(LeaveApplications.employee_id)
        .subquery()
    )

    # Remaining leaves for each employee
    remaining_leaves_sub = (
        select(
            LeaveDetails.employee_id,
            func.sum(RemainingLeaves.remaining_leaves).label("remaining_leaves")
        )
        .join(RemainingLeaves, RemainingLeaves.leave_detail_id == LeaveDetails.id)
        .group_by(LeaveDetails.employee_id)
        .subquery()
    )

    # Final query
    query = (
        select(
            User.employee_id,
            User.name.label("employee_name"),
            total_leaves_taken_sub.c.total_leaves_taken,
            func.coalesce(remaining_leaves_sub.c.remaining_leaves, 0).label("remaining_leaves"),
            func.coalesce(
                func.string_agg(
                    func.concat(
                        leave_type_breakdown.c.leave_type,
                        ':',
                        leave_type_breakdown.c.days_taken.cast(String)
                    ),
                    ', '
                ),
                ''
            ).label("leave_types")
        )
        .join(total_leaves_taken_sub, User.employee_id == total_leaves_taken_sub.c.employee_id)
        .outerjoin(remaining_leaves_sub, User.employee_id == remaining_leaves_sub.c.employee_id)
        .outerjoin(leave_type_breakdown, User.employee_id == leave_type_breakdown.c.employee_id)
        .group_by(
            User.employee_id,
            User.name,
            total_leaves_taken_sub.c.total_leaves_taken,
            remaining_leaves_sub.c.remaining_leaves
        )
    )

    result = await db.execute(query)
    return result.fetchall()