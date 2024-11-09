from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os
from agents.water_data_agent import water_agent, WaterDataRequest

app = FastAPI(title="Kenya Water Monitoring API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Kenya Water Monitoring API"}

@app.post("/water-data")
async def get_water_data(country: str = "KEN", year: int = datetime.now().year):
    try:
        request = WaterDataRequest(country=country, year=year)
        response = await water_agent.get_data(request)
        
        if not response:
            raise HTTPException(
                status_code=404,
                detail="No data available"
            )
        
        return {
            "success": True,
            "data": response.dict() if hasattr(response, 'dict') else response
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "agent_status": "running",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )