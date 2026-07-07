from fastapi import FastAPI, status,HTTPException
from pydantic import BaseModel, Field
from datetime import datetime

app = FastAPI()
tickets_db = [
    {"id": 1, "movie_name": "Doctor Strange 3", "room_code": "IMAX-01", "quantity": 2, "status": "confirmed", "created_at": "2026-07-01T19:00:00Z"},
    {"id": 2, "movie_name": "Avatar 3", "room_code": "PREMIUM-02", "quantity": 1, "status": "confirmed", "created_at": "2026-07-01T20:15:00Z"}
]


@app.get("/tickets", status_code=  status.HTTP_200_OK)
def display():
    return {
        "statusCode": 200,
        "message": "Lấy danh sách vé thành công!",
        "data": tickets_db,
        "error": "null",
        "timestamp": datetime.now().isoformat(),
        "path": "/tickets"
    }

class Ticket(BaseModel):
    id: int
    movie_name: str = Field(...,min_length=3)
    room_code: str = Field(...,min_length=3)
    quantity: int = Field(...,ge=1,le=10)
    status: str
    created_at: str

@app.post("/tickets", status_code=status.HTTP_201_CREATED,response_model=Ticket)
def add_ticket(ticket: Ticket):
    data = [
        t for t in tickets_db if t["movie_name"] == ticket.movie_name or t["room_code"] == ticket.room_code
    ]
    if data:
        raise HTTPException (
            status_code=400,
            detail={
    "statusCode": 400,
    "message": "Lỗi: Vé xem phim tại phòng chiếu này đã được đặt!",
    "data": None,
    "error": "ERR-CINE-01: Ticket conflict for movie and room combination.",
    "timestamp": datetime.now().isoformat(),
    "path": "/tickets"
}
        )
    ticket.id = tickets_db[-1]["id"] + 1
    ticket.created_at = datetime.now().isoformat()
    ticket.status = "confirmed"
    new_ticket = ticket.model_dump()
    tickets_db.append(new_ticket)
    return {
        "statusCode": 201,
        "message": "Đặt vé thành công!",
        "data": new_ticket,
        "error": "null",
        "timestamp": ticket.created_at,
        "path": "/tickets"
    }

@app.delete("/tickets/{ticket_id}", status_code=status.HTTP_200_OK)
def delete_ticket(ticket_id : int):
    ticket = next((t for t in tickets_db if t["id"] == ticket_id), None)
    
        
    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "statusCode": 404,
                "message": "Lỗi: Không tìm thấy mã vé yêu cầu!",
                "data": None,
                "error": "ERR-CINE-02: Ticket ID does not exist.",
                "timestamp": datetime.now().isoformat(),
                "path": f"/tickets/{ticket_id}"
            }
        )
    tickets_db.remove(ticket)
