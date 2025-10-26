"""
AUREX.AI - Alerts API Endpoints.
"""

from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Query
from loguru import logger
from pydantic import BaseModel, Field
from sqlalchemy import desc, select

from packages.db_core.cache import get_cache
from packages.db_core.connection import db_manager
from packages.db_core.models import Alert

router = APIRouter()


class AlertCreate(BaseModel):
    """Alert creation model."""

    type: str = Field(..., description="Alert type (price_spike, price_drop, sentiment_shift)")
    severity: str = Field(..., description="Severity (low, medium, high)")
    message: str = Field(..., description="Alert message")
    metadata: dict = Field(default_factory=dict, description="Additional metadata")


class AlertResponse(BaseModel):
    """Alert response model."""

    id: int
    timestamp: str
    type: str
    severity: str
    message: str
    metadata: dict
    acknowledged: bool
    acknowledged_at: str | None


@router.get("/")
async def get_alerts(
    hours: int = Query(24, ge=1, le=720, description="Hours of alerts to fetch"),
    severity: str = Query(None, description="Filter by severity"),
    acknowledged: bool = Query(None, description="Filter by acknowledged status"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=200, description="Items per page"),
):
    """
    Get alerts.

    Args:
        hours: Number of hours of alerts
        severity: Filter by severity
        acknowledged: Filter by acknowledged status
        page: Page number
        page_size: Number of items per page

    Returns:
        dict: Alerts with pagination
    """

    try:
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)

        async with db_manager.get_session() as session:
            # Build query
            query = select(Alert).where(Alert.timestamp >= cutoff_time)

            if severity:
                query = query.where(Alert.severity == severity)

            if acknowledged is not None:
                query = query.where(Alert.acknowledged == acknowledged)

            # Count total
            count_result = await session.execute(query)
            total_count = len(count_result.scalars().all())

            # Fetch page
            query = (
                query.order_by(desc(Alert.timestamp))
                .offset((page - 1) * page_size)
                .limit(page_size)
            )

            result = await session.execute(query)
            alerts = result.scalars().all()

            alert_data = [
                {
                    "id": a.id,
                    "timestamp": a.timestamp.isoformat(),
                    "type": a.type,
                    "severity": a.severity,
                    "message": a.message,
                    "metadata": a.alert_metadata,
                    "acknowledged": a.acknowledged,
                    "acknowledged_at": a.acknowledged_at.isoformat() if a.acknowledged_at else None,
                }
                for a in alerts
            ]

            return {
                "status": "success",
                "data": alert_data,
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total_items": total_count,
                    "total_pages": (total_count + page_size - 1) // page_size,
                },
                "params": {
                    "hours": hours,
                    "severity": severity,
                    "acknowledged": acknowledged,
                },
            }

    except Exception as e:
        logger.error(f"Error fetching alerts: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/")
async def create_alert(alert: AlertCreate):
    """
    Create a new alert.

    Args:
        alert: Alert data

    Returns:
        dict: Created alert
    """

    try:
        async with db_manager.get_session() as session:
            new_alert = Alert(
                timestamp=datetime.utcnow(),
                type=alert.type,
                severity=alert.severity,
                message=alert.message,
                alert_metadata=alert.metadata,
            )

            session.add(new_alert)
            await session.commit()
            await session.refresh(new_alert)

            return {
                "status": "success",
                "data": {
                    "id": new_alert.id,
                    "timestamp": new_alert.timestamp.isoformat(),
                    "type": new_alert.type,
                    "severity": new_alert.severity,
                    "message": new_alert.message,
                    "metadata": new_alert.alert_metadata,
                },
            }

    except Exception as e:
        logger.error(f"Error creating alert: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{alert_id}")
async def get_alert_by_id(alert_id: int):
    """
    Get an alert by ID.

    Args:
        alert_id: Alert ID

    Returns:
        dict: Alert details
    """

    try:
        async with db_manager.get_session() as session:
            query = select(Alert).where(Alert.id == alert_id)
            result = await session.execute(query)
            alert = result.scalar_one_or_none()

            if not alert:
                raise HTTPException(status_code=404, detail="Alert not found")

            return {
                "status": "success",
                "data": {
                    "id": alert.id,
                    "timestamp": alert.timestamp.isoformat(),
                    "type": alert.type,
                    "severity": alert.severity,
                    "message": alert.message,
                    "metadata": alert.alert_metadata,
                    "acknowledged": alert.acknowledged,
                    "acknowledged_at": alert.acknowledged_at.isoformat() if alert.acknowledged_at else None,
                },
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching alert by ID: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch("/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: int):
    """
    Acknowledge an alert.

    Args:
        alert_id: Alert ID

    Returns:
        dict: Updated alert
    """

    try:
        async with db_manager.get_session() as session:
            query = select(Alert).where(Alert.id == alert_id)
            result = await session.execute(query)
            alert = result.scalar_one_or_none()

            if not alert:
                raise HTTPException(status_code=404, detail="Alert not found")

            alert.acknowledged = True
            alert.acknowledged_at = datetime.utcnow()

            await session.commit()
            await session.refresh(alert)

            return {
                "status": "success",
                "data": {
                    "id": alert.id,
                    "acknowledged": alert.acknowledged,
                    "acknowledged_at": alert.acknowledged_at.isoformat(),
                },
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error acknowledging alert: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{alert_id}")
async def delete_alert(alert_id: int):
    """
    Delete an alert.

    Args:
        alert_id: Alert ID

    Returns:
        dict: Success message
    """

    try:
        async with db_manager.get_session() as session:
            query = select(Alert).where(Alert.id == alert_id)
            result = await session.execute(query)
            alert = result.scalar_one_or_none()

            if not alert:
                raise HTTPException(status_code=404, detail="Alert not found")

            await session.delete(alert)
            await session.commit()

            return {
                "status": "success",
                "message": f"Alert {alert_id} deleted successfully",
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting alert: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

