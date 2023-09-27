import psycopg2
from psycopg2.extensions import connection
import config

def init(db: connection):
    cur = None
    try:
        cur = db.cursor()

        cur.execute("""
            CREATE SEQUENCE IF NOT EXISTS property_seq
            START WITH 1
            INCREMENT BY 1
            MINVALUE 1
            MAXVALUE 100;
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS PROPERTY (
                PID INTEGER NOT NULL DEFAULT nextval('property_seq'),
                PName VARCHAR(255) NOT NULL, 
                PAddress VARCHAR(255) NOT NULL,
                CONS_DATE DATE NOT NULL,
                PRIMARY KEY (PID)
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS OWNERS (
                TC INTEGER PRIMARY KEY,
                FirstName VARCHAR(255) NOT NULL,
                Surname VARCHAR(255) NOT NULL,
                Phone INTEGER NOT NULL,
                PID INTEGER,
                FOREIGN KEY (PID) REFERENCES PROPERTY(PID) ON DELETE CASCADE
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS COMPANY (
                CID INTEGER PRIMARY KEY,
                CName VARCHAR(255) NOT NULL,
                CLocation VARCHAR(255) NOT NULL
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS DEMOLISH (
                DID INTEGER PRIMARY KEY,
                PID INTEGER,
                CID INTEGER,
                DDate DATE NOT NULL,
                DPrice DECIMAL(10,2),
                FOREIGN KEY (PID) REFERENCES PROPERTY(PID) ON DELETE CASCADE,
                FOREIGN KEY (CID) REFERENCES COMPANY(CID) ON DELETE CASCADE
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS BUILD (
                BID INTEGER PRIMARY KEY,
                PID INTEGER,
                CID INTEGER,
                BDate DATE NOT NULL,
                BPrice DECIMAL(10,2),
                FOREIGN KEY (PID) REFERENCES PROPERTY(PID) ON DELETE CASCADE,
                FOREIGN KEY (CID) REFERENCES COMPANY(CID) ON DELETE CASCADE
            );
        """)

        cur.execute("""
        INSERT INTO OWNERS (TC, FirstName, Surname, Phone, PID) 
VALUES (1,'John','Doe','555-555-5555',1),
       (2,'Jane','Doe','555-555-5556',2),
       (3,'Bob','Smith','555-555-5557',3),
       (4,'Samantha','Johnson','555-555-5558',4),
       (5,'Michael','Williams','555-555-5559',5),
       (6,'Emily','Jones','555-555-5560',6),
       (7,'Matthew','Brown','555-555-5561',7),
       (8,'Ashley','Davis','555-555-5562',8),
       (9,'Joshua','Miller','555-555-5563',9),
       (10,'Nicholas','Garcia','555-555-5564',10);
        """)

        cur.execute("""
        INSERT INTO PROPERTY (PID, PName, PAddress, CONS_DATE) 
VALUES (1,'Property 1','Address 1','2022-01-01'),
       (2,'Property 2','Address 2','2022-01-02'),
       (3,'Property 3','Address 3','2022-01-03'),
       (4,'Property 4','Address 4','2022-01-04'),
       (5,'Property 5','Address 5','2022-01-05'),
       (6,'Property 6','Address 6','2022-01-06'),
       (7,'Property 7','Address 7','2022-01-07'),
       (8,'Property 8','Address 8','2022-01-08'),
       (9,'Property 9','Address 9','2022-01-09'),
       (10,'Property 10','Address 10','2022-01-10');
        """)

        cur.execute("""
        INSERT INTO COMPANY (CID, CName, CLocation) 
VALUES (1,'Company 1','Location 1'),
       (2,'Company 2','Location 2'),
       (3,'Company 3','Location 3'),
       (4,'Company 4','Location 4'),
       (5,'Company 5','Location 5'),
       (6,'Company 6','Location 6'),
       (7,'Company 7','Location 7'),
       (8,'Company 8','Location 8'),
       (9,'Company 9','Location 9'),
       (10,'Company 10','Location 10');
        """)

        cur.execute("""
        INSERT INTO DEMOLISH (DID, PID, CID, DDate, DPrice) 
VALUES (1,1,1,'2022-01-01',1000),
       (2,2,2,'2022-01-02',2000),
       (3,3,3,'2022-01-03',3000),
       (4,4,4,'2022-01-04',4000),
       (5,5,5,'2022-01-05',5000),
       (6,6,6,'2022-01-06',6000),
       (7,7,7,'2022-01-07',7000),
       (8,8,8,8,'2022-01-08',8000),
       (9,9,9,'2022-01-09',9000),
       (10,10,10,'2022-01-10',10000);
        """)

        cur.execute("""
        INSERT INTO BUILD (BID, PID, CID, BDate, BPrice)
VALUES (1,1,1,'2022-01-01',1000),
(2,2,2,'2022-01-02',2000),
(3,3,3,'2022-01-03',3000),
(4,4,4,'2022-01-04',4000),
(5,5,5,'2022-01-05',5000),
(6,6,6,'2022-01-06',6000),
(7,7,7,'2022-01-07',7000),
(8,8,8,'2022-01-08',8000),
(9,9,9,'2022-01-09',9000),
(10,10,10,'2022-01-10',10000);
        """)

         

        cur.execute("""
            CREATE VIEW IF NOT EXISTS OwnerProperties AS
            SELECT O.TC, P.PName
            FROM OWNERS O
            JOIN PROPERTY P
            ON O.PID = P.PID;
        """)

        cur.execute("""
        CREATE FUNCTION IF NOT EXISTS get_property_details (pid INTEGER)
        RETURNS TABLE (PID2 INTEGER, PName2 VARCHAR(255), PAddress2 VARCHAR(255), CONS_DATE2 DATE) as $$
        BEGIN
            RETURN QUERY SELECT PID, PName, PAddress, CONS_DATE
            FROM PROPERTY
            WHERE PID = pid2;
        END;
        $$ LANGUAGE 'plpgsql';
        """)

        cur.execute("""
        CREATE FUNCTION IF NOT EXISTS count_build_by_cid (cid INTEGER)
        RETURNS INTEGER as $$
		DECLARE counter INTEGER;
        BEGIN
            SELECT COUNT(*) INTO counter
            FROM BUILD B
            WHERE CID = cid;
            RETURN counter;
        END;
		$$ LANGUAGE 'plpgsql';
        """)

        db.commit()
    except Exception as er:
        print(er)
        return False
    finally:
        if cur is not None:
            cur.close()

def db_connect():
    try:
        db = psycopg2.connect(
                            host = config.host,
                            dbname = config.database,
                            user = config.username,
                            password = config.pwd,
                            port = config.port
            )
        return db
    except Exception as er:
        print(er)
        return None


####################################################################################
################################# INSERT FUNCTIONS #################################
####################################################################################
def insert_owner(db: connection,TC: int, fname: str, lname: str, phone: int, PID: int):
    cur = None
    try:
        cur = db.cursor()
        query = """
                    INSERT INTO OWNERS (TC, FirstName, Surname, Phone, PID)
                    VALUES (%s, %s, %s, %s, %s); """
        values = (TC, fname, lname, phone, PID)
        cur.execute(query,values)
        db.commit()
        return True
    except Exception as er:
        print(er)
        return False
    finally:
        if cur is not None:
            cur.close()

def insert_property(db: connection, name: str, address: str, cons_date: str):
    cur = None
    try:
        cur = db.cursor()
        query = """
                    INSERT INTO PROPERTY (PName, PAddress, CONS_DATE)
                    VALUES (%s, %s, %s); """
        values = (name,address,cons_date)
        cur.execute(query,values)
        db.commit()
        return True
    except Exception as er:
        print(er)
        return False
    finally:
        if cur is not None:
            cur.close()

def insert_company(db: connection, CID: int, name: str, location: str):
    cur = None
    try:
        cur = db.cursor()
        query = """
                    INSERT INTO COMPANY (CID, CName, CLocation)
                    VALUES (%s, %s, %s); """
        values = (CID,name,location)
        cur.execute(query,values)
        db.commit()
        return True
    except Exception as er:
        print(er)
        return False
    finally:
        if cur is not None:
            cur.close()

def insert_build(db: connection, bid: int, bdate: str, pid: int, cid: int, bprice: int):
    cur = None
    try:
        cur = db.cursor()
        query = """
                    INSERT INTO BUILD (BID, BDate, PID, CID, BPrice)
                    VALUES (%d, %s, %d, %d, %d); """
        values = (bid,bdate,pid,cid,bprice)
        cur.execute(query,values)
        db.commit()
        return True
    except Exception as er:
        print(er)
        return False
    finally:
        if cur is not None:
            cur.close()

def insert_demolish(db: connection, did: int, ddate: str, pid: int, cid: int, dprice: int):
    cur = None
    try:
        cur = db.cursor()
        query = """
                    INSERT INTO DEMOLISH (DID, DDate, PID, CID, dPrice)
                    VALUES (%d, %s, %d, %d, %d); """
        values = (did,ddate,pid,cid,dprice)
        cur.execute(query,values)
        db.commit()
        return True
    except Exception as er:
        print(er)
        return False
    finally:
        if cur is not None:
            cur.close()

def add_menu(db: connection):
    flag = True
    while flag:
        print("1. Add new owner")
        print("2. add new property")
        print("3. add new build project")
        print("4. add new demolish project")
        print("5. add new company")
        print("6. Go back")
        choise = int(input("please make selection: "))
        
        if choise == 1:
            tc = int(input("enter TC: "))
            fname = input("enter first name: ")
            lname = input("enter last name: ")
            phone = int(input("enter phone number (only numbers): "))
            pid = int(input("enter PID (Property id): "))
            res = insert_owner(db,tc,fname,lname,phone,pid)
        elif choise == 2:
            name = input("enter property name: ")
            address = input("enter property address: ")
            cons_date = input("enter property construction date: ")
            res = insert_property(db,name,address,cons_date)
        elif choise == 3:
            bid = int(input("enter BID (Build id): "))
            bdate =input("enter buld date: ")
            pid = int(input("enter PID (Property id): "))
            cid = int(input("enter CID (Company id): "))
            price = int(input("enter build price: "))
            res = insert_build(db,bid,bdate,pid,cid,price)
        elif choise == 4:
            did = int(input("enter DID (Demolish id): "))
            bdate =input("enter Demolish date: ")
            pid = int(input("enter PID (Property id): "))
            cid = int(input("enter CID (Company id): "))
            cost = int(input("enter Demolish cost: "))
            res = insert_build(db,did,bdate,pid,cid,cost)
        elif choise == 5:
            cid = int(input("enter company id: "))
            name = input("enter company name: ")
            location = input("enter company location: ")
            res = insert_company(db,cid,name,location)
        elif choise == 6:
            flag = False
        else:
            print("invalid selection")
        if res:
            res = False
            db.commit()
            print("your data has been added successfully\n\n")
    return True


#############################################################################
################################# SHOW DATA #################################
#############################################################################
def select_query(db: connection, table_name: str):
    cur = None
    try:
        cur = db.cursor()
        query = "SELECT * FROM " + table_name
        value = (table_name,)
        cur.execute(query)
        res = cur.fetchall()
        # print(res)
        return res
    except psycopg2.Error as er:
        # db.rollback()
        print(er)
        return False
    finally:
        if cur is not None:
            cur.close()

def show_menu(db: connection):
    flag = True
    while flag:
        data = False
        print("1. show owners data")
        print("2. show properties data")
        print("3. show build projects data")
        print("4. show demolish projects data")
        print("5. show companies data")
        print("6. show owners properties data")
        print("7. Go back")
        choise = int(input("please make selection: "))
        
        if choise == 1:
            data = select_query(db,"OWNERS")
        elif choise == 2:
            data = select_query(db,"PROPERTY")
        elif choise == 3:
            data = select_query(db,"BUILD")
        elif choise == 4:
            data = select_query(db,"DEMOLISH")
        elif choise == 5:
            data = select_query(db,"COMPANY")
        elif choise == 6:
            data = select_query(db,"OwnerProperties")
        elif choise == 7:
            flag = False
        else:
            print("invalid selection")
        
        if data is not False:
            print("data: ")
            for record in data:
                print(record)


############################################################################
############################## DELETE SECTION ##############################
############################################################################
def delete_demolish(db: connection, did: int):
    cur = None
    try:
        cur = db.cursor()
        query = """
                    DELETE FROM DEMOLISH
                    WHERE DID = %s; """
        values = (did,)
        cur.execute(query,values)
        db.commit()
        return True
    except Exception as er:
        print(er)
        return False
    finally:
        if cur is not None:
            cur.close()

def delete_build(db: connection, bid: int):
    cur = None
    try:
        cur = db.cursor()
        query = """
                    DELETE FROM DEMOLISH
                    WHERE BID = %s; """
        values = (bid,)
        cur.execute(query,values)
        db.commit()
        return True
    except Exception as er:
        print(er)
        return False
    finally:
        if cur is not None:
            cur.close()

def delete_menu(db: connection):
    flag = True
    while flag:
        print("1. delete build project")
        print("2. delete demolish project")
        print("3. Go back")
        choise = int(input("please make selection: "))

        if choise == 1:
            did = input("enter DID: ")
            res = delete_demolish(db,did)
        elif choise == 2:
            bid = input("enter bID: ")
            res = delete_build(db,bid)
        elif choise == 3:
            flag = False
        else:
            print("invalid selection")
        if res:
            print("data deleted successfully")


############################################################################
############################## UPDATE SECTION ##############################
############################################################################
def update_com_location(db: connection,cid: int,loc: str):
    cur = None
    try:
        cur = db.cursor()
        query = """
                    UPDATE company
                    SET CLocation = %s
                    WHERE CID = %s;"""
        values = (loc,cid)
        cur.execute(query,values)
        db.commit()
        return True
    except Exception as er:
        print(er)
        return False
    finally:
        if cur is not None:
            cur.close()

def update_dprice_date(db: connection,did: int,price: int,date: str):
    cur = None
    try:
        cur = db.cursor()
        query = """
                    UPDATE DEMOLISH
                    SET DPrice = %s, DDate = %s
                    WHERE DID = %s;"""
        values = (price,date,did)
        cur.execute(query,values)
        db.commit()
        return True
    except Exception as er:
        print(er)
        return False
    finally:
        if cur is not None:
            cur.close()

def update_menu(db: connection):
    flag = True
    while flag:
        print("1. update company location")
        print("2. update demolish price and date")
        print("3. Go back")
        choise = int(input("please make selection: "))

        if choise == 1:
            cid = input("enter company id: ")
            loc = input("enter new company location: ")
            res = update_com_location(db,cid,loc)
        elif choise == 2:
            did = input("enter demolish id: ")
            cost = input("enter new demolish cost: ")
            date = input("enter new demolish date: ")
            res = update_com_location(db,did,cost,date)
        elif choise == 3:
            flag = False
        else:
            print("invalid selection")
        if res:
            print("data deleted successfully")


#############################################################################
############################### EXTRA SECTION ###############################
#############################################################################

def find(db: connection,prefix: str):
    cur = None
    try:
        cur = db.cursor()
        query = """
                    SELECT O.TC, O.Name, O.Surname
                    FROM OWNER O
                    JOIN PROPERTY P
                    ON O.PID = P.PID
                    WHERE P.PName LIKE '%s%'
                    UNION
                    SELECT O.TC, O.Name, O.Surname
                    FROM OWNER O
                    JOIN PROPERTY P
                    ON O.PID = P.PID
                    WHERE P.PName LIKE '%s%'"""
        values = (prefix.lower(), prefix.upper())
        cur.execute(query,values)
        db.commit()
        return True
    except Exception as er:
        print(er)
        return False
    finally:
        if cur is not None:
            cur.close()

def avg_price(db: connection, value: int):
    cur = None
    try:
        cur = db.cursor()
        query = """
                    SELECT C.CName, AVG(D.DPrice) as AveragePrice
                    FROM COMPANY C, DEMOLISH D
                    WHERE C.CID = D.CID 
                    GROUP BY C.CName
                    HAVING AVG(D.DPrice) < %s;"""
        values = (value)
        cur.execute(query,values)
        db.commit()
        return True
    except Exception as er:
        print(er)
        return False
    finally:
        if cur is not None:
            cur.close()

def count_build_by_cid(db: connection, value: int):
    cur = None
    try:
        cur = db.cursor()
        query = """
                    SELECT C.CName, AVG(D.DPrice) as AveragePrice
                    FROM COMPANY C, DEMOLISH D
                    WHERE C.CID = D.CID 
                    GROUP BY C.CName
                    HAVING AVG(D.DPrice) < %s;"""
        values = (value)
        cur.execute(query,values)
        db.commit()
        return True
    except Exception as er:
        print(er)
        return False
    finally:
        if cur is not None:
            cur.close()

def extra_menu(db: connection):
    flag = True
    while flag:
        print("1. get properties start with specific letter")
        print("2. get companies that has avg value lower than specific number")
        print("3. get cid by user and return number of properties being build by that cid")
        print("4. for record. returns PROPERTY table")
        print("5. Go back")
        choise = int(input("please make selection: "))

        if choise == 1:
            pre = input("enter prefix: ")
            res = find(db,pre)
        elif choise == 2:
            value = input("enter max avg value: ")
            res = update_com_location(db,value)
        elif choise == 3:
            id = input("enter id: ")
            select_query("get_property_details("+str(id)+")")
        elif choise == 4:
            value = input("enter max avg value: ")
            res = update_com_location(db,value)
        elif choise == 5:
            flag = False
        else:
            print("invalid selection")
        if res:
            print("data deleted successfully")
    

def main():
    db = db_connect()
    if db is None:
        return False

    init(db)

    print("1. Show up data")
    print("2. Add new data")
    print("3. delete some data")
    print("4. Update data")
    print("5. extra")
    choise = int(input("please make selection: "))

    
    if choise == 1:
        show_menu(db)
    elif choise == 2:
        add_menu(db)
    elif choise == 3:
        delete_menu(db)
    elif choise == 4:
        pass
    elif choise == 5:
        pass
    else:
        print("invalid selection")

    cur = db.cursor()
    cur.close()

    db.commit()
    db.close()

main()
