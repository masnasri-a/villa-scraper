from datetime import datetime
from datetime import timedelta
from fastapi import FastAPI
import requests, re, json
from test import get_data


app = FastAPI()

@app.get("/get-villa-availability")
def get_villa_availability(start: str, end: str):
    # get total nights from start and end dates
    date_format = "%Y-%m-%d"
    start_date = datetime.strptime(start, date_format).date()
    end_date = datetime.strptime(end, date_format).date()
    total_nights = (end_date - start_date).days + 1
    print(f"Total nights: {total_nights}")
    response = get_data(start, total_nights)
    if response:
        return {
            "start_date": start,
            "end_date": end,
            "total_nights": total_nights,
            "availability": response
        }
    else:
        return {"error": "No data found or an error occurred."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)