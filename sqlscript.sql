 /*Make flights table*/
CREATE TABLE airline.Flights (
    Flight_ID CHAR(6) PRIMARY KEY NOT NULL, 
    dt DATETIME (0),
    origin VARCHAR(255),
    destination VARCHAR(255),
    duration INTEGER,
    seats_avail INTEGER,
    seat_cap INTEGER,
    price INTEGER
);

/*Make Accounts table*/
CREATE TABLE airline.Accounts (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(255),
    fname VARCHAR(50),
    mname VARCHAR(50),
    lname VARCHAR(50),
    dob DATE,
    gender CHAR(1),
    address VARCHAR(255),
    city VARCHAR(255),
    state CHAR(2),
    zipcode INTEGER(5),
    email VARCHAR(255),
    phone BIGINT (11),
    paymentcard BIGINT(16),
    cvc INTEGER(3),
    expiredate DATE,
    UNIQUE KEY(paymentcard)
    /*FOREIGN KEY (paymentcard) REFERENCES airline.Reservation(paymentcard)*/
);

/*make Passengers table*/
CREATE TABLE airline.Passengers (
    Ticket_ID INTEGER(9) PRIMARY KEY,
    PNR CHAR(6),   
    username VARCHAR(50),
    fname VARCHAR(50),
    mname VARCHAR(50),
    lname VARCHAR(50),
    dob DATE,
    gender CHAR(1),
    address VARCHAR(255),
    city VARCHAR(255),
    state CHAR(2),
    zipcode INTEGER(5),
    email VARCHAR(255),
    phone BIGINT(11)
);

/*Reservation table*/
CREATE TABLE airline.Reservation (
    PNR CHAR(6) PRIMARY KEY,
    Flight_ID CHAR(6),
    purchase_date TIMESTAMP,
    paymentcard BIGINT(16),
    cvc INTEGER(3),
    expdate DATE,
    FOREIGN KEY (Flight_ID) REFERENCES airline.Flights(Flight_ID)
);
