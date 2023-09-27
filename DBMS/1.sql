------------------------------------------------------------------------LEGEND
--PID = property id
--CID = company id
--DID = demolish id
--BID = build id

--CONS_DATE = construction date of building (bina ne zaman insa edildi)
--DDate = binanin yikilacagi tarih (demolish date)
--BDate = binanin tekrar yapilacagi tarih (build date)
--BPrice, DPrice = sirket tarafindan alinan ucret (insa etmek ve yikilmak icin)


------------------------------------------------------------------------TABLE
CREATE TABLE OWNERS (
    TC INTEGER PRIMARY KEY,
    FirstName VARCHAR(255) NOT NULL,
    Surname VARCHAR(255) NOT NULL,
    Phone INTEGER NOT NULL,
    PID INTEGER,
    FOREIGN KEY (PID) REFERENCES PROPERTY(PID) ON DELETE CASCADE
);


CREATE TABLE PROPERTY (
    PID INTEGER NOT NULL DEFAULT nextval('property_seq'),
    PName VARCHAR(255) NOT NULL, 
    PAddress VARCHAR(255) NOT NULL,
    CONS_DATE DATE NOT NULL,
    PRIMARY KEY (PID)
);

CREATE TABLE COMPANY (
    CID INTEGER PRIMARY KEY,
    CName VARCHAR(255) NOT NULL,
    CLocation VARCHAR(255) NOT NULL
);

CREATE TABLE DEMOLISH (
    DID INTEGER PRIMARY KEY,
    PID INTEGER,
    CID INTEGER,
    DDate DATE NOT NULL,
    DPrice DECIMAL(10,2),
    FOREIGN KEY (PID) REFERENCES PROPERTY(PID) ON DELETE CASCADE,
    FOREIGN KEY (CID) REFERENCES COMPANY(CID) ON DELETE CASCADE
);

CREATE TABLE BUILD (
    BID INTEGER PRIMARY KEY,
    PID INTEGER,
    CID INTEGER,
    BDate DATE NOT NULL,
    BPrice DECIMAL(10,2),
    FOREIGN KEY (PID) REFERENCES PROPERTY(PID) ON DELETE CASCADE,
    FOREIGN KEY (CID) REFERENCES COMPANY(CID) ON DELETE CASCADE
);

-------------------------------------------------------------------------------- SEQUENCE
CREATE SEQUENCE property_seq
START WITH 1
INCREMENT BY 1
MINVALUE 1
MAXVALUE 100;
