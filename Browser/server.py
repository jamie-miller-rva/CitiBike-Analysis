import psycopg2
try:
    connection = psycopg2.connect(user = "gfsxlvmtqwnogp",
                                  password = "534030f82dc0d74634d2253fa43f403ecbd9dd50346f7c140a3564d03c2a2506",
                                  host = "ec2-184-73-169-163.compute-1.amazonaws.com",
                                  port = "5432",
                                  database = "d806adirak8md8")
    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print ( connection.get_dsn_parameters(),"\n")
    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")