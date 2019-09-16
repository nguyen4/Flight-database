import mysql.connector
import datetime

#establishes connection to Database
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password",
    database = "airline"
)

#searchs all flights with same start, end, and date of depart
def QueryFlights(data):
    cursor = mydb.cursor()
    # data tuple format -> (departing city, arriving city, date of depart 'yyyy-mm-dd')

    cursor.execute("""
            SELECT 
                * 
            FROM airline.flights
            WHERE 
                origin = %s AND destination = %s AND DATE(dt) = %s""", data)
    result = cursor.fetchall()

    cursor.close()
    return result

def isFlightAvail(flightID):
    
    cursor = mydb.cursor()

    cursor.execute("""
            SELECT 
                * 
            FROM airline.flights
            WHERE
                Flight_ID = %s AND seats_avail > 0""", (flightID,))
    results = cursor.fetchall()

    print('\n\n')
    
    if len(results) == 0:
        cursor.close()
        return False
    else:
        cursor.close()
        return True

def showPrice(flightID):

    cursor = mydb.cursor()

    cursor.execute("""
            SELECT price
            FROM airline.flights
            WHERE Flight_ID = %s""", (flightID,))
    results = cursor.fetchall()

    return results[0][0]

def updateSeat(flightID):
    cursor = mydb.cursor()

    cursor.execute("""
        UPDATE airline.flights AS a
        NATURAL JOIN airline.flights AS b
        SET a.seats_avail = b.seats_avail - 1
        WHERE a.Flight_ID = %s""", (flightID,))

    mydb.commit()
    cursor.close()

def getRowFromReservation(pnr):
    cursor = mydb.cursor()

    cursor.execute("""
        SELECT * 
        FROM airline.Reservation
        WHERE PNR = %s""", (pnr,))
    results = cursor.fetchall()

    cursor.close()
    return results #list of tuples

def getRowFromPassengers(ticketID):
    cursor = mydb.cursor()

    cursor.execute("""
        SELECT * 
        FROM airline.Passengers
        WHERE Ticket_ID = %s""", (ticketID,))
    results = cursor.fetchall()

    cursor.close()
    return results #list of tuples

def addNewPassenger(data):
    cursor = mydb.cursor()

    cursor.execute("""
        INSERT INTO airline.Passengers 
        (Ticket_ID, PNR, username, fname, lname, mname, dob, gender, address, city, state, zipcode, email, phone)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (data))
    
    mydb.commit()
    cursor.close()

def addNewReservation(data):
    cursor = mydb.cursor()

    cursor.execute("""
        INSERT INTO airline.Reservation
        (PNR, Flight_ID, purchase_date, paymentcard, cvc, expdate)
        VALUES (%s, %s, %s, %s, %s, %s)""",
        (data))
    
    mydb.commit()
    cursor.close()
    
def reservationExists(data):
    #data has (pnr, firstname, lastname)
    cursor = mydb.cursor()

    query = """SELECT * FROM airline.Reservation R 
    INNER JOIN airline.Passengers P 
    ON R.pnr = P.pnr
    WHERE P.PNR = %s AND P.fname = %s AND P.lname = %s"""

    cursor.execute(query, data)
    results = cursor.fetchall()

    cursor.close()
    if len(results) == 0:
        return False
    else:
        return True

def getTicketID(data):
    cursor = mydb.cursor()

    query = """
        SELECT P.Ticket_ID FROM airline.Reservation R 
        INNER JOIN airline.Passengers P 
        ON R.pnr = P.pnr
        WHERE P.PNR = %s AND P.fname = %s AND P.lname = %s"""

    cursor.execute(query, data)
    results = cursor.fetchall()
    cursor.close()
    return results[0]


def getReservationInfo(pnr):
    #data has (pnr, firstname, lastname)
    cursor = mydb.cursor()

    #get tuple of Reservation 
    query = """
        SELECT F.dt, F.origin, F.destination, F.duration, F.price, R.purchase_date
        FROM airline.Flights F INNER JOIN airline.Reservation R
        ON F.Flight_ID = R.Flight_ID
        WHERE R.PNR = %s"""
    
    cursor.execute(query, (pnr,))
    results = cursor.fetchall()
    return results[0]
    #get tuple of flight info (dt, origin, destination, duration, price)
