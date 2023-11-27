CREATE TABLE Airline (
    AirlineName varchar(255),
    PRIMARY KEY (AirlineName)
);
CREATE TABLE Airport (
    AirportCode varchar(50),
    Name varchar(255),
    City varchar(255),
    Country varchar(255),
    NumTerminals int,
    Type varchar(255),
    PRIMARY KEY (AirportCode)
);
CREATE TABLE Airplane (
    PlaneID int,
    AirlineName varChar(255),
    NumSeats int,
    Manufacturer varchar(255),
    ModelNum varchar(255),
    ManuDate DATE,
    Age int,
    FOREIGN KEY (AirlineName) REFERENCES `Airline`(AirlineName),
    UNIQUE (PlaneID)
);
CREATE TABLE Flight (
    AirlineName varchar(255),
    FlightNum int,
    DepartureTime DATETIME,
    DepartureAirport varchar(255),
    ArrivalTime DATETIME,
    ArrivalAirport varchar(255),
    BasePrice float(6, 2),
    Status varchar(255),
    PlaneID int,
    FOREIGN KEY (AirlineName) REFERENCES `Airline`(AirlineName),
    FOREIGN KEY (PlaneID) REFERENCES `Airplane`(PlaneID),
    UNIQUE (FlightNum)
);
CREATE TABLE Maintenance (
    PlaneID int,
    MaintenanceID varchar(255),
    Start DATETIME,
    End DATETIME,
    FOREIGN KEY (PlaneID) REFERENCES `Airplane`(PlaneID),
    UNIQUE (MaintenanceID)
);
CREATE TABLE Customer (
    Email varchar(255),
    Password varchar(255),
    FirstName varchar(255),
    LastName varchar(255),
    BuildingNum int,
    Street varchar(255),
    AptNum int,
    City varchar(255),
    State varchar(255),
    Zipcode int,
    PassportNumber int,
    PassportExpiration DATE,
    PassportCountry varchar(255),
    DateOfBirth DATE,
    PRIMARY KEY (Email)
);
CREATE TABLE CustomerPhone (
    Email varchar(255),
    PhoneNumber varchar(20),
    FOREIGN KEY (Email) REFERENCES `Customer`(Email)
);
CREATE TABLE Ticket (
    TicketID varchar(255),
    FlightNum int,
    PRIMARY KEY (TicketID),
    FOREIGN KEY (FlightNum) REFERENCES `Flight`(FlightNum)
);
CREATE TABLE Purchase (
    TicketID varchar(255),
    Email varchar(255),
    CardType varchar(255),
    CardNum varchar(255),
    CardExp DATE,
    CardName varchar(255),
    PurchaseTime DATETIME,
    CalculatedPrice float(6, 2),
    FirstName varchar(255),
    LastName varchar(255),
    DateOfBirth DATE,
    FOREIGN KEY (TicketID) REFERENCES `Ticket`(TicketID),
    FOREIGN KEY (Email) REFERENCES `Customer`(Email)
);
CREATE TABLE AirlineStaff (
    Username varchar(255),
    Password varchar(255),
    AirlineName varchar(255),
    FirstName varchar(255),
    LastName varchar(255),
    DateOfBirth DATE,
    FOREIGN KEY (AirlineName) REFERENCES `Airline`(AirlineName),
    PRIMARY KEY (Username)
);
CREATE TABLE StaffContact (
    Username varchar(255),
    PhoneNumber varchar(255),
    Email varchar(255),
    FOREIGN KEY (Username) REFERENCES `AirlineStaff`(Username)
);
CREATE TABLE Rating (
    Email varchar(255),
    Rating int,
    FlightNum int,
    Comment varchar(255),
    FOREIGN KEY (Email) REFERENCES `Customer`(Email),
    FOREIGN KEY (FlightNum) REFERENCES `Flight`(FlightNum)
);
CREATE TABLE Departures AS
    SELECT f.AirlineName, a.AirportCode, f.FlightNum, f.DepartureTime
    FROM `Flight` as f, `Airport` as a;
CREATE TABLE Arrivals AS
    SELECT f.AirlineName, a.AirportCode, f.FlightNum, f.ArrivalTime
    FROM `Flight` as f, `Airport` as a;