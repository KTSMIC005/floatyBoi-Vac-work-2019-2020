
# import influxdb
from influxdb import InfluxDBClient
import json

testing = False
if testing:
    import sys
    # insert at 1, 0 is the script path (or '' in REPL)
    # sys.path.insert(1, r'C:\Users\micha\University of Cape Town\floatyBoi Vac work 2019-2020 - Documents\Python Code\InfluxPython')
    # import data_fetcher_fake.py
else:
    import data_fetcher_fake







def make_database(client,database_name):
    databases = client.get_list_database()
    has_db = False
    for db in databases:
        if (db["name"] == database_name):
            has_db = True
            break

    if has_db:
        return "Already has db"

    try:
        client.create_database(database_name)
    except:
        return 1
    else:
        return "Some error reached. Is the database server online?"
    
    



def main():
    client = InfluxDBClient(host='localhost', port=8086 )

    this_db = 'pyexample'
    msg = make_database(client, this_db)
    if(1 != msg):
        print(msg)

    print("List of avalible databases")
    print(client.get_list_database())

    client.switch_database(this_db)


    # Do something to get data

    if(not testing):
        pass
    
    new_data = data_fetcher_fake.get_recent_data() 
    dta =  new_data
    # print(json.loads(dta))   
    print(dta)   
    # print(dta.reverse)

    # print(client.write_points(new_data))
    client.write_points(new_data)

    client.que


    




    
    



if __name__ == "__main__":
    # Do some stuff
    # Then run the main
    main()