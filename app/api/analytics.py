from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from app.services.test import analytics_service, test_taking_service
from app.core.middleware import get_current_user  # Add this import

router = APIRouter()

@router.get("/tests/{test_id}", response_model=Dict)
async def get_test_analysis(test_id: str, user = Depends(get_current_user)):
    #  In a real implementation, ensure the test belongs to the user
    #  and fetch test results from a database.
    try:
        test_results = await test_taking_service.get_test_results(test_id, user["user_id"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    analysis = await analytics_service.analyze_test_performance(test_results)
    return analysis

@router.get("/history", response_model=List[Dict])
async def get_performance_history(user = Depends(get_current_user)):
    return await analytics_service.get_historical_performance(user["user_id"])


@router.get("/dashboard", response_model=Dict)
async def get_analytics_dashboard(user = Depends(get_current_user)):
    #  Combine test analysis and historical data for a dashboard view
    #  In a real application, you might want to allow filtering by topic, time range, etc.
    historical_data = await analytics_service.get_historical_performance(user["user_id"])
    # Get analysis of the most recent test (or allow user to specify)
    if historical_data:
        try:
            latest_test_results = await test_taking_service.get_test_results(historical_data[-1]["test_id"], user["user_id"])
            latest_analysis = await analytics_service.analyze_test_performance(latest_test_results)
        except ValueError:
            latest_analysis = {} # Handle case where results might not be available yet
    else:
        latest_analysis = {} # No test history

    dashboard_data = await analytics_service.prepare_performance_data_for_visualization(latest_analysis, historical_data)
    return dashboard_data