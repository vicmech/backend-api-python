import logging
from mysql.connector import Error
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from database import getConnection, closeConnection
from metrics import solvingTime, attendingTime
from typing import Optional
from pydantic import BaseModel

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

class CaseCreate(BaseModel):
    reporter_id: int
    manager_id: int
    register_date: str
    atention_date: Optional[str]
    close_date: Optional[str]
    priority: str
    description: str
    status: str

class ReporterCreate(BaseModel):
    reporter_id: Optional[int]
    reporter_first_name: str
    reporter_last_name: str
    reporter_sex : str
    reporter_age : int

class CaseManagerCreate(BaseModel):
    manager_id: int
    manager_first_name: str
    manager_last_name: str
    manager_sex : str

class CombinedCreate(BaseModel):
    reporter_first_name: str
    reporter_last_name: str
    reporter_age: int
    reporter_sex: str
    manager_id: int
    register_date: str
    priority: str
    description: str
    status: str

# REPORTS routes
@app.get("/api/reports/{report_id}") #Individual Report
async def read_item(report_id: int):
    try:
        Con = getConnection()
        cursor = Con.cursor()
        cursor.execute(f'SELECT * FROM reports WHERE report_id={report_id}')
        item = cursor.fetchone()
        return item
    except Error as e:
        logging.error(e)
        print(e)
    finally:
        closeConnection(Con)

@app.get("/api/reports/") #Reports by status and/or priority
async def read_item(status: str = None, priority: str = None):
    try:
        Con = getConnection()
        cursor = Con.cursor()

        query = "SELECT * FROM reports WHERE 1=1"
        params = []
        if status:
            query += " AND LOWER(status)=LOWER(%s)"
            params.append(status)
        if priority:
            query += " AND LOWER(priority)=LOWER(%s)"
            params.append(priority)
        
        cursor.execute(query, params)
        items = cursor.fetchall()
        return items
    except Error as e:
        logging.error(e)
    finally:
        closeConnection(Con)

@app.get("/api/reports/solvingTime/{report_id}") #Solving time for a report
async def read_item(report_id: int):
    try:
        Con = getConnection()
        cursor = Con.cursor()
        cursor.execute(f'SELECT * FROM reports WHERE report_id={report_id}')
        item = cursor.fetchone()
        return solvingTime(item)
    except Error as e:
        logging.error(e)
    finally:
        closeConnection(Con)

@app.get("/api/reports/attendingTime/{report_id}") #Attending time for a report
async def read_item(report_id: int):
    try:
        Con = getConnection()
        cursor = Con.cursor()
        cursor.execute(f'SELECT * FROM reports WHERE report_id={report_id}')
        item = cursor.fetchone()
        return attendingTime(item)
    except Error as e:
        logging.error(e)
    finally:
        closeConnection(Con)

@app.get("/api/reports/registerDate/") #Getting reports by date
async def getReportByDate(year : Optional[int] = None, month : Optional[int] = None, day : Optional[int] = None):
    try:
        Con = getConnection()
        cursor = Con.cursor()
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
    except Error as e:
        logging.error(e)
    finally:
        closeConnection(Con)



# REPORTERS routes
@app.get("/api/reporters/") #Get all reporters or by id, name or lastname
async def read_item(id : int = None, name : str = None, lastname : str = None):
    try:
        Con = getConnection()
        cursor = Con.cursor()
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

        cursor.execute(query, params)
        items = cursor.fetchall()
        return items
    except Error as e:
        logging.error(e)
    finally:
        closeConnection(Con)

# CASEMANAGERS routes
@app.get("/api/casemanagers/") #Get all casemanagers or by id, name or lastname
async def read_item(id : int = None, name : str = None, lastname : str = None):
    try:
        Con = getConnection()
        cursor = Con.cursor()
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
    
        cursor.execute(query, params)
        items = cursor.fetchall()
        return items
    except Error as e:
        logging.error(e)
    finally:
        closeConnection(Con)

#POST method to create a new report
@app.post("/api/report/create/")
async def create_case(case: CombinedCreate, response : Response):
    try:
        con = getConnection()
        cursor = con.cursor()
        response.headers["Access-Control-Allow-Origin"] = "*"
        query = """INSERT INTO reporters (reporter_first_name, reporter_last_name, reporter_sex, reporter_age) VALUES (%s, %s, %s, %s)"""
        values = (case.reporter_first_name, case.reporter_last_name, case.reporter_sex, case.reporter_age)
   
        cursor.execute(query, values)
        con.commit()
        logging.info("Reporter created successfully with id: " + str(cursor.lastrowid))
        reporter_id = cursor.lastrowid
    except Error as e:
        logging.error(e)
        logging.error("Reporter could not be created")
        print(e)
        return "No se pudo crear el reportero"
    finally:
        closeConnection(con)

    try:
        con = getConnection()
        cursor = con.cursor()
        query = """
        INSERT INTO reports (reporter_id, manager_id, register_date, priority, description, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = [
            reporter_id,
            case.manager_id,
            case.register_date,
            case.priority,
            case.description,
            case.status
        ]
        cursor.execute(query, values)
        con.commit()
        logging.info("Case created successfully")
    except Error as e:
        logging.error("Case could not be created")
        logging.error(e)
        print(e)
    finally:
        closeConnection(con)