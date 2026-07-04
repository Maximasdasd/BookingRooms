from fastapi import FastAPI



app = FastAPI(
    title="Booking Rooms Service",
    version="1.0.0",
    description="API для бронирования переговорных",
)


@app.get("/")
def root():
    return {
        "message": "Booking Rooms Service",
        "docs": "/docs",
        "version": "1.0.0",
    }
        

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("bookingroom.main:app", host="0.0.0.0", port=8000, reload=True)
