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

class CaseManagerCreate(BaseModel):
    supporter_id: str
    supporter_name: str
    supporter_lastname: str
    supporter_department : str

class CombinedCreate(BaseModel):
    isNewClient: bool
    client_id: Optional[str]
    client_name: Optional[str]
    client_lastname: Optional[str]
    client_age: Optional[str]
    client_document: str
    client_sex: Optional[str]
    client_city: Optional[str]
    ticket_id : str
    ticket_supporter: str
    ticket_generation_date: str
    ticket_category: str
    ticket_description: Optional[str]

# Tickets routes
@app.get("/api/tickets/") #Reports by status and/or priority
async def read_item(
    ticket_id: Optional[str] = None,
    client_id: Optional[str] = None,
    supporter_id: Optional[str] = None,
    ticket_register_date: Optional[str] = None,
    ticket_close_date: Optional[str] = None,
    ticket_status: Optional[str] = None,
    ticket_category: Optional[str] = None,
):
    try:
        Con = getConnection()
        cursor = Con.cursor()

        query = "SELECT * FROM tickets WHERE 1=1"
        params = []
        if ticket_id is not None:
            query += " AND ticket_id = %s"
            params.append(ticket_id)
        if client_id is not None:
            query += " AND ticket_client_id = %s"
            params.append(client_id)
        if supporter_id is not None:
            query += " AND ticket_supporter = %s"
            params.append(supporter_id)
        if ticket_register_date is not None:
            query += " AND DATE(ticket_register_date) = %s"
            params.append(ticket_register_date)
        if ticket_close_date is not None:
            query += " AND DATE(ticket_close_date) = %s"
            params.append(ticket_close_date)
        if ticket_status is not None:
            query += " AND LOWER(ticket_status)=LOWER(%s)"
            params.append(ticket_status)
        if ticket_category is not None:
            query += " AND LOWER(ticket_category)=LOWER(%s)"
            params.append(ticket_category)

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
@app.get("/api/clients/") #Get all reporters or by id, name or lastname
async def read_item(client_id : str = None, name : str = None, lastname : str = None, document : str = None):
    try:
        Con = getConnection()
        cursor = Con.cursor()
        query = "SELECT * FROM clients WHERE 1=1"
        params = []
        if client_id is not None:
            query += " AND client_id=%s"
            params.append(client_id)
        if name is not None:
            query += " AND LOWER(client_name)=LOWER(%s)"
            params.append(name)
        if lastname is not None:
            query += " AND LOWER(client_lastname)=LOWER(%s)"
            params.append(lastname)
        if document is not None:
            query += " AND LOWER(client_document)=%s"
            params.append(document)

        cursor.execute(query, params)
        items = cursor.fetchall()
        return items
    except Error as e:
        logging.error(e)
    finally:
        closeConnection(Con)

# CASEMANAGERS routes
@app.get("/api/supporters/") #Get all casemanagers or by id, name or lastname
async def read_item(id : str = None, name : str = None, lastname : str = None, department : str = None):
    try:
        Con = getConnection()
        cursor = Con.cursor()
        query = "SELECT * FROM supporters WHERE 1=1"
        params = []
        if id:
            query += " AND supporter_id=%s"
            params.append(id)
        if name:
            query += " AND LOWER(supporter_name)=LOWER(%s)"
            params.append(name)
        if lastname:
            query += " AND LOWER(supporter_lastname)=LOWER(%s)"
            params.append(lastname)
        if department:
            query += " AND lower(supporter_department)=LOWER(%s)"
            params.append(department)
    
        cursor.execute(query, params)
        items = cursor.fetchall()
        return items
    except Error as e:
        return []
        logging.error(e)
    finally:
        closeConnection(Con)

# DEPARTMENTS routes
@app.get("/api/departments/")
async def get_departments(department_id : Optional[str] = None):
    try:
        print(department_id)
        con = getConnection()
        cursor = con.cursor()
        query = 'SELECT * FROM departments WHERE 1=1'
        params = []

        if(department_id is not None):
            query += ' AND department_id = %s'
            params.append(department_id)

        cursor.execute(query, params)
        items = cursor.fetchall()
        return items
    except Error as e:
        logging.error(e)
    finally:
        closeConnection(con)

@app.get("/api/getGraph2/")
async def get_data():
    try:
        con = getConnection()
        cursor = con.cursor()
        cursor.execute("SELECT t.ticket_category AS Categoria, SUM(CASE WHEN c.client_sex = 'Masculino' THEN 1 ELSE 0 END) AS Casos_Masculinos, SUM(CASE WHEN c.client_sex = 'Femenino' THEN 1 ELSE 0 END) AS Casos_Femeninos FROM `delivery-cases-db`.tickets t INNER JOIN `delivery-cases-db`.clients c ON t.ticket_client_id = c.client_id GROUP BY t.ticket_category")
        items = cursor.fetchall()
        return items
    except Error as e:
        logging.error(e)
    finally:
        closeConnection(con)

@app.get("/api/getGraph3/")
async def get_data():
    try:
        con = getConnection()
        cursor = con.cursor()
        cursor.execute("SELECT `delivery-cases-db`.c.client_sex AS Sexo, SUM(CASE WHEN t.ticket_generation_date >= DATE_SUB(CURDATE(), INTERVAL 4 WEEK) THEN 1 ELSE 0 END) AS Semana_4, SUM(CASE WHEN t.ticket_generation_date >= DATE_SUB(CURDATE(), INTERVAL 3 WEEK) AND t.ticket_generation_date < DATE_SUB(CURDATE(), INTERVAL 2 WEEK) THEN 1 ELSE 0 END) AS Semana_3, SUM(CASE WHEN t.ticket_generation_date >= DATE_SUB(CURDATE(), INTERVAL 2 WEEK) AND t.ticket_generation_date < DATE_SUB(CURDATE(), INTERVAL 1 WEEK) THEN 1 ELSE 0 END) AS Semana_2, SUM(CASE WHEN t.ticket_generation_date >= DATE_SUB(CURDATE(), INTERVAL 1 WEEK) THEN 1 ELSE 0 END) AS Semana_1 FROM `delivery-cases-db`.tickets t INNER JOIN `delivery-cases-db`.clients c ON t.ticket_client_id = c.client_id GROUP BY c.client_sex;")
        items = cursor.fetchall()
        return items
    except Error as e:
        logging.error(e)
    finally:
        closeConnection(con)

#POST method to create a new report
@app.post("/api/tickets/create/")
async def create_case(ticket: CombinedCreate, response : Response):

    client_id = ticket.client_id or None
    client_name = ticket.client_name or None
    client_lastname = ticket.client_lastname or None  
    client_age = ticket.client_age or None
    client_document = ticket.client_document
    client_sex = ticket.client_sex or None
    client_city = ticket.client_city or None
    ticket_id = ticket.ticket_id
    ticket_supporter = ticket.ticket_supporter
    ticket_generation_date = ticket.ticket_generation_date
    ticket_category = ticket.ticket_category
    ticket_description = ticket.ticket_description or None

    print(client_id)
    if(ticket.isNewClient):
        try:
            con = getConnection()
            cursor = con.cursor()
            response.headers["Access-Control-Allow-Origin"] = "*"
            query = """INSERT INTO clients (client_id, client_name, client_lastname, client_document, client_sex, client_age, client_city) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            values = (
                client_id,
                client_name,
                client_lastname,
                client_document,
                client_sex,
                client_age,
                client_city)
        
            cursor.execute(query, values)
            con.commit()
            logging.info("Client created successfully with id: " + client_id)
        except Error as e:
            logging.error(e)
            logging.error("Reporter could not be created")
            print(e)
            return "No se pudo crear el reportero"
        finally:
            closeConnection(con)
    else:
        try:
            con = getConnection()
            cursor = con.cursor()
            query = 'SELECT * FROM clients WHERE client_document = %s'
            cursor.execute(query, [ticket.client_document])
            ticket.client_id = cursor.fetchone()
        except Error as e:
            logging.error(e)
        finally:
            closeConnection(con)

    try:
        con = getConnection()
        print('connected')
        cursor = con.cursor()
        query = """
        INSERT INTO tickets (ticket_id, ticket_category, ticket_supporter, ticket_status, ticket_description, ticket_generation_date, ticket_client_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = [
            ticket_id,
            ticket_category,
            ticket_supporter,
            'Abierto',
            ticket_description,
            ticket_generation_date,
            client_id
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

@app.post('/api/supporters/create')
async def create_manager(supporter : CaseManagerCreate):
    try:
        con = getConnection()
        cursor = con.cursor()
        query = """INSERT INTO supporters (supporter_id, supporter_name, supporter_lastname, supporter_department) VALUES (%s, %s, %s, %s)"""
        values = (supporter.supporter_id,
                  supporter.supporter_name,
                  supporter.supporter_lastname,
                  supporter.supporter_department)
   
        cursor.execute(query, values)
        con.commit()
        logging.info("Supporter created successfully")
    except Error as e:
        logging.error('Supporter could not be created')
        logging.error(e)
    finally:
        closeConnection(con)

