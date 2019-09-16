import sys
import sqlQueries
import datetime
import random
import string

def DisplayMenu():

    print("******************************************")
    print("*Welcome to the Flight Reservation Kiosk!*")
    print("******************************************")
    print("*Please make a selection:                *")
    print("*(1) Search Flights                      *")
    print("*(2) Book a Flight                       *")
    print("*(3) Check Current or Past Resrvations   *")
    print("*(4) Exit Program / Logout               *")
    print("******************************************")

    selection = int(input())

    return selection

def MakeSelection(i):
    if i == 1:
        return SearchFlightsPage()
    elif i == 2:
        return BookFlight()
    elif i == 3:
        return checkReservationsDisplay()
    elif i == 4:
        print("Thank you for using the Flight Reservation Kiosk. Goodbye!")
        return sys.exit()
    else:
        print("Invalid input")
        return main()

def SearchFlightsPage():

    print("Search Flights chosen")
    
    flight = sqlQueries.QueryFlights(SearchFlights())

    if len(flight) == 0:
        print('There are no flights available. \nReturning to main menu')
    else:
        print('\n\n')
        for x in flight:
            print("Flight ID: " + str(x[0]) + 
                "\t|Date: " + str(x[1]) + 
                "\t|Origin: " + str(x[2]) + 
                "\t|Destination: " + str(x[3]) + 
                "\t|Duration: " + str(x[4]) + 
                "\t|Seats Available: " + str(x[5]) + 
                "\tSeat Capacity: " + str(x[6]) + 
                "\tPrice: " + str(x[7]))
            print('\n')
        print('\n\n')
    main()


def SearchFlights():
    
    departing_city = input("Enter the derparture city: ")
    arriving_city = input("Enter the arrival city: ")

    while departing_city == arriving_city:
        departing_city = input("Enter the derparture city: ")
        arriving_city = input("Enter the arrival city: ")
    
    date_str = input("Enter the date of departure (mm/dd/yyyy): ") 

    # turn date into datetime object
    date = datetime.datetime.strptime(date_str, '%m/%d/%Y').date()

    # returns a tuple
    return (departing_city, arriving_city, date)

def BookFlight():
    print("Book Flight chosen")
    
    #get flight num from user
    flight_num = input("Enter a flight ID: ")
    
    #if flight does not exist, update the seats available for that flight
    if not sqlQueries.isFlightAvail(flight_num):
        print('\n\n')
        print("No Flight with that ID in database")
        print("Returning to main menu")
        print('\n\n')
        main()
    
    #show price
    print("Price of Flight:" + str(sqlQueries.showPrice(flight_num)))
    buy = input("Would you like to buy a ticket? (Y/N): ")
    
    if buy.upper() == 'N':
        main()

    #insert new rows into Passenger and Reservation table
    data1 = EnterInfo()
    data2 = EnterPaymentInfo()
    buyTicket(flight_num, data1, data2)
    sqlQueries.updateSeat(flight_num)

    return main

def EnterInfo():
    print("******************************************")
    print("              Passenger INFO              ")
    print("******************************************")
    firstname = input("Enter your first name: ")
    lastname = input("Enter your last name: ")
    middlename = input("Enter your middle name or none: ")
    dob = datetime.datetime.strptime(input("Enter your dob: mm/dd/yyyy: "),'%m/%d/%Y').date()
    gender = input("What is your gender(M/F/N)?: ")
    address = input("Enter your address (EX 1234 Beverly Hills Suite 129): ")
    city = input("City?: ")
    state = input("2-letter State (Ex. FL for Florida): ")
    zipcode = int(input("Zip code?: "))
    email = input("Email (Ex. mysql@jmail.com): ")
    phonenum = int(input("Phone: (Ex. 1239999999): "))

    if(middlename == 'none'):
        middlename = None
    

    return (firstname,
            lastname,
            middlename,
            dob,
            gender,
            address,
            city,
            state,
            zipcode,
            email,
            phonenum)

def EnterPaymentInfo():
    print("******************************************")
    print("               Payment INFO               ")
    print("******************************************")
    cc = int(input("Credit/debit card number: "))
    cvc = int(input("3-digit CVC (located on back of card): "))
    expiredate = datetime.datetime.strptime(input("Expiration date (MM/YYYY): "), '%m/%Y').date()

    return (cc, cvc, expiredate)

def checkReservation():

    selection = checkReservationsDisplay()


def checkReservationsDisplay():

    print("*******************************")
    print("*   Do you have an Account?   *")
    print("*-----------------------------*")
    print("*Enter a Selection            *")
    print("*(1) YES, LOGIN               *")
    print("*(2) Create an Account        *")
    print("*(3) Continue as Guest        *")
    print("*******************************")

    selection = int(input())

    return selectionReservation(selection)

def selectionReservation(s):

    if s == 1:
        return MyFlights()
    elif s == 2:
        return main()
    elif s == 3:
        return findReservation()
    else:
        return main()

def findReservation():

    pnr = input("Enter your pnr: ")
    fn = input("Enter your first name: ")
    ln = input("Enter your last name: ")

    data = (pnr, fn, ln)
    #check if passenger for flight exists
    if not sqlQueries.reservationExists(data):
        print('No Reservation for pnr' + pnr)
        return main()
    
    ticketID = sqlQueries.getTicketID(data)
    resData = sqlQueries.getReservationInfo(pnr)
    resInfo = ticketID + data + resData
    printReservation(resInfo)

    return main()

def printReservation(data):
    tk = str(data[0])
    pnr = str(data[1])
    origin = data[5]
    destination = data[6]
    ddate = str(data[4].date())
    dtime = str(data[4].time())
    adate = str((data[4] + datetime.timedelta(minutes=(data[7]))).date())
    atime = str((data[4] + datetime.timedelta(minutes=(data[7]))).time())
    board = str((data[4] - datetime.timedelta(minutes=30)).time())    
    paid = str(data[8])
    paiddate = str(data[9].date())
    print('\n\n')
    print('TICKET NUMBER:' + tk)
    print('PNR:' + pnr)
    print('-----------------------------------------------------')
    print('Flight info')
    print('-----------------------------------------------------')
    print('FROM: ' + origin + '\t\tTO: ' + destination)
    print('Depart Date:' + ddate + '\t\tDepart Time: ' + dtime)
    print('Arrival Date:' + adate + '\t\tArrival Time: ' + atime)
    print('Boarding Time: ' + board)
    print('Price of Ticket: ' + paid + '\t\tPaid on:' + paiddate)
    print('\n\n')

def buyTicket(flight_ID, data1, data2):

    pnr = generateNewPNR()
    purchaseDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ticket_ID = generateNewTicketID()

    #create new tuple for passenger
    passengerData = (ticket_ID, pnr, None) + data1
    
    reservationData = (pnr, flight_ID, purchaseDate) + data2
    #create new tuple for reservation

    sqlQueries.addNewPassenger(passengerData)
    sqlQueries.addNewReservation(reservationData)

    print('\n\n')
    print('Payment processed')
    print('Ticket bought')
    print('Your PNR is: ' + str(pnr))
    print('\n\n')

def generateNewTicketID():
    ticketID = ''.join(random.choice(string.digits) for _ in range(9))
    results = sqlQueries.getRowFromPassengers(ticketID)

    while len(results) != 0:
        ticketID = ''.join(random.choice(string.digits) for _ in range(9))
        results = sqlQueries.getRowFromPassengers(ticketID)
    return ticketID

def generateNewPNR():
    pnr = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    results = sqlQueries.getRowFromReservation(pnr)

    while len(results) != 0:
        pnr = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        results = sqlQueries.getRowFromReservation(pnr)
    
    return pnr
 
def MyFlights():
    auth = UserLogin()
    if not auth:
        DisplayFlights(auth)
    else:
        print("No user with these credentials\n returning to menu\n\n")    
    return main()

def UserLogin():
    userEmail = input("Email: ")
    userPassword = input("Password: ")

    cursor = sqlQueries.mydb.cursor()
    cursor.execute("SELECT * From Accounts")
    result = cursor.fetchall()
    cursor.close()
 
    for row in result:
        if(row[0] == userEmail and row[1] == userPassword):
            return (row[12])
    
def DisplayFlights(cardNum):
    cursor = sqlQueries.mydb.cursor()
    cursor.execute("""SELECT * From Reservation WHERE paymentcard = %s""", (cardNum,))
    result = cursor.fetchall()
    cursor.close()
    for row in result:
        if(row[3] == cardNum):
            print("PNR: " + row[0] + " Flight ID" + row[1] + " Purchase Date: " + row[2])

        

def quitP():
    print("Thank you for using the Flight Reservation Kiosk. Goodbye!")
    sys.exit()

def main():

    selection = DisplayMenu()

    MakeSelection(selection)
    return

if __name__ == "__main__":
    main()