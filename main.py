from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import con, cursor
from metrics import solvingTime, attendingTime
from typing import Optional
app = FastAPI()

origins = [
    "http://localhost:3000", #nextjs domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

items = {"items": [{"name": "Item 1"}, {"name": "Item 2"}]}

# REPORTS routes
@app.get("/api/reports/{report_id}") #Individual Report
async def read_item(report_id: int):
    cursor.execute(f'SELECT * FROM reports WHERE report_id={report_id}')
    item = cursor.fetchone()
    return item

@app.get("/api/reports/") #Reports by status and/or priority
async def read_item(status: str = None, priority: str = None):
    query = "SELECT * FROM reports WHERE 1=1"
    params = []
    if status:
        query += " AND LOWER(status)=LOWER(%s)"
        params.append(status)
    if priority:
        query += " AND LOWER(priority)=LOWER(%s)"
        params.append(priority)
    
    try:
        cursor.execute(query, params)
        items = cursor.fetchall()
        return items
    except:
        return "No hay reportes con ese estado"

@app.get("/api/reports/solvingTime/{report_id}") #Solving time for a report
async def read_item(report_id: int):
    try:
        cursor.execute(f'SELECT * FROM reports WHERE report_id={report_id}')
        item = cursor.fetchone()
        return solvingTime(item)
    except:
        return "El reporte no ha sido cerrado"

@app.get("/api/reports/attendingTime/{report_id}") #Attending time for a report
async def read_item(report_id: int):
    try:
        cursor.execute(f'SELECT * FROM reports WHERE report_id={report_id}')
        item = cursor.fetchone()
        return attendingTime(item)
    except:
        return "El reporte no ha sido atendido"
    
@app.get("/api/reports/registerDate/") #Getting reports by date
async def getReportByDate(year : Optional[int] = None, month : Optional[int] = None, day : Optional[int] = None):
    try:
        query = "SELECT * FROM reports WHERE 1=1"
        params = []
    
        if year:
            query += " AND YEAR(register_date) = %s"
            params.append(year)
        if month:
            query += " AND MONTH(register_date) = %s"
            params.append(month)
        if day:
            query += " AND DAY(register_date) = %s"
            params.append(day)
        
        cursor.execute(query, params)
        items = cursor.fetchall()
        return items
    except:
        return "No hay reportes en ese mes"
    



# REPORTERS routes
@app.get("/api/reporters/") #Get all reporters or by id, name or lastname
async def read_item(id : int = None, name : str = None, lastname : str = None):
    query = "SELECT * FROM reporters WHERE 1=1"
    params = []
    if id:
        query += " AND reporter_id=%s"
        params.append(id)
    if name:
        query += " AND LOWER(reporter_first_name)=LOWER(%s)"
        params.append(name)
    if lastname:
        query += " AND LOWER(reporter_last_name)=LOWER(%s)"
        params.append(lastname)
    
    try:
        cursor.execute(query, params)
        items = cursor.fetchall()
        return items
    except:
        return "No hay reporteros con esas especificaciones"


# CASEMANAGERS routes
@app.get("/api/casemanagers/") #Get all casemanagers or by id, name or lastname
async def read_item(id : int = None, name : str = None, lastname : str = None):
    query = "SELECT * FROM casemanager WHERE 1=1"
    params = []
    if id:
        query += " AND manager_id=%s"
        params.append(id)
    if name:
        query += " AND LOWER(manager_first_name)=LOWER(%s)"
        params.append(name)
    if lastname:
        query += " AND LOWER(manager_last_name)=LOWER(%s)"
        params.append(lastname)
    
    try:
        cursor.execute(query, params)
        items = cursor.fetchall()
        return items
    except:
        return "No hay reporteros con esas especificaciones"
    
@app.get("/api/casemanagers/avg/") #Get the average service quality for each casemanager
async def read_item(): 
    cursor.execute(f"SELECT manager_id, ROUND(AVG(TRIM(service_quality)), 2) AS promedioCalidadServicio FROM reports GROUP BY manager_id")
    item = cursor.fetchall()
    return item


@app.post("/api/items")
async def create_item(item: dict):
    # Procesa el nuevo item (por ejemplo, guardarlo en la base de datos)
    items["items"].append(item)
    return {"message": "Item creado"}