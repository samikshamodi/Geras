import mysql.connector
from tabulate import tabulate
import requests
import json
import time
from datetime import datetime



mydb=mysql.connector.connect(host="localhost", user="root",passwd="samiksha",database="geras")
#"db is the database name in mysql on my computer. You might have named it as project or geras in yours"
print(mydb)
sql_cursor = mydb.cursor()

def pretty_print_results(results, column_names_list):
    print(tabulate(results, headers=column_names_list, tablefmt='fancy_grid'))


#------------------------------------------------------------------------------------------------------------------
# ELDERLY
def register_an_elderly(sql_cursor,aadhar_no,first_name,last_name,dob,mobile,house_no,street_name,city,state,zip):
    query =  ''' INSERT INTO Elderly(aadhar_no,first_name,last_name,dob,mobile_no,house_no,street_name,city,state,zip) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''

    params = [aadhar_no,first_name,last_name,dob,mobile,house_no,street_name,city,state,zip]

    try:
        sql_cursor.execute(query, params)
        mydb.commit()
        print("Welcome to our app Geras. Thank you for registering.")
    except Exception as e:
        print(e)
        return


def request_service_by_elderly(sql_cursor,service_ID, details, service_status, aadhar_no,start_date):
    query =  ''' INSERT INTO Service(service_ID, details, service_status, aadhar_no, start_date) VALUES (%s,%s,%s,%s,%s);'''

    params = [service_ID, details, service_status,aadhar_no,start_date]

    try:
        sql_cursor.execute(query, params)
        mydb.commit()
        print("Your service request has been recorded")
    except Exception as e:
        print(e)
        return


def track_service_request_of_an_elderly(sql_cursor, ser_ID):
    query =  '''SELECT * FROM SERVICE WHERE Service_ID = %s;'''

    params = [ser_ID]

    try:
        sql_cursor.execute(query, params)
        results = sql_cursor.fetchall()
    except Exception as e:
        print(e)
        return

    return list(results), sql_cursor.column_names

def get_presecription_history_of_an_elderly(sql_cursor,aadhar_no):
    query =  ''' SELECT * FROM Medicine_Update where aadhar_no=%s;'''
    params = [aadhar_no]

    try:
        sql_cursor.execute(query, params)
        results = sql_cursor.fetchall()
    except Exception as e:
        print(e)
        return

    return list(results), sql_cursor.column_names


def update_prescription_of_an_elderly(sql_cursor, aadhar_no, date, prescription,doctor_name):
    query =  ''' REPLACE INTO Medicine_Update(Aadhar_No,Date,Prescription,Doctor_Name) VALUES (%s,%s,%s,%s);'''

    params = [aadhar_no, date, prescription, doctor_name]

    try:
        sql_cursor.execute(query, params)
        mydb.commit()
        print("Updated prescription of "+ aadhar_no)
    except Exception as e:
        print(e)
        return

def get_service_history_of_an_elderly(sql_cursor,aadhar_no):
    query =  ''' SELECT * FROM Service where aadhar_no=%s;'''
    params = [aadhar_no]

    try:
        sql_cursor.execute(query, params)
        results = sql_cursor.fetchall()
    except Exception as e:
        print(e)
        return

    return list(results), sql_cursor.column_names



def get_all_completed_services_of_an_elderly(sql_cursor,aadhar_no):
    query =  ''' SELECT * FROM Service where aadhar_no=%s and service_status='completed';'''
    params = [aadhar_no]

    try:
        sql_cursor.execute(query, params)
        results = sql_cursor.fetchall()
    except Exception as e:
        print(e)
        return

    return list(results), sql_cursor.column_names

def get_all_pending_services_of_an_elderly(sql_cursor,aadhar_no):
    query =  ''' SELECT * FROM Service where aadhar_no=%s and (service_status='inprogress' or service_status='requested');'''
    params = [aadhar_no]

    try:
        sql_cursor.execute(query, params)
        results = sql_cursor.fetchall()
    except Exception as e:
        print(e)
        return

    return list(results), sql_cursor.column_names

def dergister_an_elderly(sql_cursor, aadhar_no):
    query =  ''' Update Elderly SET status='inactive' where aadhar_no=%s'''
    params = [aadhar_no]

    try:
        sql_cursor.execute(query, params)
        mydb.commit()
        print("We're sorry to see you go.")
    except Exception as e:
        print(e)
        return


#Volunteer
def register_volunteer(sql_cursor,Volunteer_ID,First_Name, Last_Name, Mobile_No, Email_ID, House_No, Street_Name, City, State, Zip):
    query = '''INSERT INTO Volunteer(Volunteer_ID,First_Name,Last_Name,Mobile_No,Email_ID,House_No,Street_Name,City,State,Zip) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
    params = [Volunteer_ID,First_Name,Last_Name,Mobile_No,Email_ID,House_No,Street_Name,City,State,Zip]
    try:
        sql_cursor.execute(query,params)
        mydb.commit()
        print("Welcome to our app Geras. Thank you for registering.")
    except Exception as e:
        print(e)
        return

def reg_volunteer_with_ngo(sql_cursor,Volunteer_ID, NGO_ID):
    query = '''REPLACE INTO Volunteer_NGO(Volunteer_ID, NGO_ID,AVAILABLE) VALUES(%s, %s,'yes');'''
    params = [Volunteer_ID, NGO_ID]
    try:
        sql_cursor.execute(query,params)
        mydb.commit()
        print("You have been successfully registered")
    except Exception as e:
        print(e)
        return

def unregister_volunteer(sql_cursor, Volunteer_ID, NGO_ID):
    query = '''UPDATE Volunteer_NGO SET Available = 'No' WHERE Volunteer_ID = %s AND NGO_ID = %s;'''
    params = [Volunteer_ID,NGO_ID]
    try:
        sql_cursor.execute(query,params)
        mydb.commit()
        print("You are no longer a volunteer for NGO with ID",NGO_ID)
    except Exception as e:
        print(e)
        return

def view_volunteer_work(sql_cursor, Volunteer_ID):
    query = '''SELECT Service_ID, Details, Start_Date FROM Service
WHERE Service_ID =
(SELECT Service_ID
FROM appoints_ngo
WHERE Volunteer_ID = %s
AND Is_Completed = 'no');'''
    params = [Volunteer_ID]
    try:
        sql_cursor.execute(query,params)
        results = sql_cursor.fetchall()
    except Exception as e:
        print(e)
        return
    return list(results), sql_cursor.column_names

def report_completion_by_volunteer(sql_cursor,Volunteer_ID, Service_ID, End_Date):
    query = '''UPDATE Appoints_NGO SET Is_Completed = 'Yes' WHERE Volunteer_ID = %s AND Service_ID = %s;'''
    params = [Volunteer_ID, Service_ID]
    try:
        sql_cursor.execute(query,params)
        mydb.commit()
        print("Work done!")
    except Exception as e:
        print(e)
        return

def update_volunteer_availability(sql_cursor,Volunteer_ID):
    ans = 'no'
    while(1):
        av = input("Enter 1 for available and 0 for unavailable: ")
        if(av=='1'):
            ans = 'yes'
            break
        elif(av=='0'):
            ans = 'no'
            break
        else:
            print("Please enter a valid option!")
    query = '''UPDATE Volunteer_NGO SET Available = %s WHERE Volunteer_ID = %s;'''
    params = [ans,Volunteer_ID]
    try:
        sql_cursor.execute(query,params)
        mydb.commit()
        print("Your status have been successfully updated")
    except Exception as e:
        print(e)
        return

#GOVT

def register_officers(sql_cursor, Officer_ID, First_Name, Last_Name, Designation, Mobile_No, House_No, Street_Name, City, State, Pincode, Email):
    query =  ''' INSERT INTO Government_Officer(Officer_ID, First_Name, Last_Name, Designation, Mobile_No, House_No, Street_Name, City, State, Pincode, Email, Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'Active');'''
    params = [Officer_ID, First_Name, Last_Name, Designation, Mobile_No, House_No, Street_Name, City, State, Pincode, Email, Status]
    try:
        sql_cursor.execute(query, params)
        mydb.commit()
        print("Welcome to Geras. Thank you for registering Officer.")
    except Exception as e:
        print(e)
        return

def access_service_request(sql_cursor,Service_ID):
    query =  '''SELECT * FROM Service WHERE Service_ID = %s;'''
    params = [Service_ID]
    try:
        sql_cursor.execute(query, params)
        results = sql_cursor.fetchall()
    except Exception as e:
        print(e)
    return list(results), sql_cursor.column_names

def assign_hw(sql_cursor, Service_ID):
    query = '''SELECT HW_ID FROM Healthcare_Worker ORDER BY RAND() ;'''
    #params = [Service_ID]
    try:
        sql_cursor.execute(query)#params)
        results = sql_cursor.fetchone()
        mydb.commit()
    except Exception as e:
        print(e)

    query2 = '''UPDATE Appoints_HW SET HW_ID = results WHERE Service_ID = %s;'''
    params = [Service_ID]
    try:
        sql_cursor.execute(query, params)
        #results = sql_cursor.fetchone()
        mydb.commit()
    except Exception as e:
        print(e)
    return

def assign_ngo(sql_cursor, Issue_Type, Service_ID):
    query = '''SELECT NGO_ID FROM NGO WHERE Issue_Type = %s ORDER BY RAND() LIMIT 1 ;'''
    params = [Issue_Type]
    try:
        sql_cursor.execute(query, params)
        results = sql_cursor.fetchone()
        mydb.commit()
    except Exception as e:
        print(e)

    query2 = '''UPDATE Appoints_NGO SET NGO_ID = results WHERE Service_ID = %s;'''
    params2 = [Service_ID]
    try:
        sql_cursor.execute(query2, params2)
        #results = sql_cursor.fetchone()
        mydb.commit()
    except Exception as e:
        print(e)
    return

def complete_transaction_hw(sql_cursor, Transaction_ID, Service_ID):
    query = '''UPDATE Appoints_HW SET Transaction_ID = %s WHERE (Service_ID = %s AND Transaction_ID = NULL)'''
    params = [Transaction_ID, Service_ID]
    try:
        sql_cursor.execute(query,params)
        mydb.commit()
        print("Transaction (" +Transaction_ID+") has been completed")
    except Exception as e:
        print(e)
    return

def complete_transaction_ngo(sql_cursor, Transaction_ID, Service_ID):
    query = '''UPDATE Appoints_NGO SET Transaction_ID = %s WHERE (Service_ID = %s AND Transaction_ID = NULL)'''
    params = [Transaction_ID, Service_ID]
    try:
        sql_cursor.execute(query,params)
        mydb.commit()
        print("Transaction (" +Transaction_ID+") has been completed")
    except Exception as e:
        print(e)
    return

def all_transactions(sql_cursor):
    query =  '''SELECT hw.Service_ID as ServiceID, hw.Transaction_ID, hw.serice_cost FROM Appoints_HW as hw UNION ngo.Service_ID as ServiceID, ngo.Transaction_ID, ngo.serice_cost FROM Appoints_NGO as ngo ORDER BY ServiceID'''
    #params = [Service_ID]
    try:
        sql_cursor.execute(query, params)
        results = sql_cursor.fetchall()
    except Exception as e:
        print(e)
        return
    return list(results), sql_cursor.column_names

def get_number_of_completed_and_pending_services(sql_cursor):
    query =  '''SELECT Service_ID, Service_Status FROM Service WHERE (Service_Status = 'Completed' OR Service_Status = 'inprogress') GROUP BY Service_Status;'''
    #params = []
    try:
        sql_cursor.execute(query, params)
        results = sql_cursor.fetchall()
    except Exception as e:
        print(e)
        return
    
    return list(results), sql_cursor.column_names

#######################

while(1):
    print("\n\nWelcome to Geras")
    print("Choose the option to proceed")
    print("1. Enter as Elderly \n2. Enter as Volunteer \n3. Enter as Government Officer \n4. Enter as NGO \n5. Enter as Family \n6. Enter as Healthcare Worker \n7. Exit Application")
    op1=int(input("Your Option: "))


    #Elderly
    if(op1==1):
        print("\n \n------------------------------\nWelcome Elderly")
        while(1):
            print("\n\nChoose the option to proceed")
            print("1. Register and add their details \n2. Request a service \n3. Get prescription \n4. Update prescription \n5. Get service history \n6. Track a particular service by service ID  \n7. Get all completed services \n8. Get all pending services \n9. SOS \n10. Go back to Main Menu")
            op2=int(input("Your Option: "))

            if(op2==1):
                aadhar=input("Enter aadhar no: ")
                fname=input("Enter first name: ")
                lname=input("Enter last name: ")
                dob=input("Enter dob in yyyymmdd: ")
                mobile=input("Enter mobile no: ")
                house=input("Enter house no: ")
                street=input("Enter street name: ")
                city=input("Enter city name: ")
                state=input("Enter state name: ")
                zip=input("Enter zip: ")

                #today=time.strftime('%Y-%m-%d')
                birth=datetime.strptime(dob,'%Y%m%d')
                today=datetime.today()
                age=((today-birth)/365).days
                if(age<60):
                    print("You must atleast be 60 years old")
                else:
                    register_an_elderly(sql_cursor,aadhar,fname,lname,dob,mobile,house,street,city,state,zip)



            elif (op2==2):
                query =  ''' SELECT * FROM Service;'''

                try:
                    sql_cursor.execute(query)
                    results = sql_cursor.fetchall()
                except Exception as e:
                    print(e)

                number=int((len(results)))
                number+=1
                #print(number)
                number='SER'+str(number)
                #print(number)

                details=input("Describe service: ")
                aadhar=input("Enter aadhar no for whom the service is requested: ")
                date=time.strftime('%Y%m%d')
                #print(date)

                request_service_by_elderly(sql_cursor,number,details,'Requested', aadhar,date)



            elif (op2==3):
                aadhar=input("Enter aadhar no: ")
                pretty_print_results(*get_presecription_history_of_an_elderly(sql_cursor,aadhar))



            elif (op2==4):
                aadhar=input("Enter aadhar no: ")
                date=time.strftime('%Y%m%d')
                prescription=input("Enter prescription: ")
                doctor=input("Enter doctor name: ")
                update_prescription_of_an_elderly(sql_cursor,aadhar,date,prescription,doctor)



            elif (op2==5):
                aadhar=input("Enter aadhar no: ")   #'237867112793
                pretty_print_results(*get_service_history_of_an_elderly(sql_cursor,aadhar))



            elif (op2==6):
                service=input("Enter service ID: ")
                pretty_print_results(*track_service_request_of_an_elderly(sql_cursor,service))



            elif (op2==7):
                aadhar=input("Enter aadhar no: ")   #'237867112793
                pretty_print_results(*get_all_completed_services_of_an_elderly(sql_cursor,aadhar))



            elif (op2==8):
                aadhar=input("Enter aadhar no: ")   #'237867112793
                pretty_print_results(*get_all_pending_services_of_an_elderly(sql_cursor,aadhar))



            elif (op2==9):
                r= requests.get('https://www.geojs.io')

                # print(r)

                ip_request=requests.get('https://get.geojs.io/v1/ip.json')

                # print(ip_request)

                ip_address=ip_request.json()['ip']

                # ip_address

                url='https://get.geojs.io/v1/ip/geo/' + ip_address + '.json'

                geo_request=requests.get(url)

                latitude=geo_request.json()['latitude']

                longitude=geo_request.json()['longitude']

                lat=float(latitude)
                lng=float(longitude)

                #add api key here
                API_KEY = 'AIzaSyBt6D3IPoGk5uHGEIPxGM-DavezZveO2CY'

                google_places = GooglePlaces(API_KEY)

                query_result = google_places.nearby_search(
                        lat_lng ={'lat': lat, 'lng': lng},
                        radius = 5000,
                        # types =[types.TYPE_HOSPITAL] or
                        # [types.TYPE_CAFE] or [type.TYPE_BAR]
                        # or [type.TYPE_CASINO])
                        types =[types.TYPE_HOSPITAL])

                # If any attributions related
                # with search results print them
                if query_result.has_attributions:
                    print (query_result.html_attributions)


                # Iterate over the search results
                for place in query_result.places:
                    # print(type(place))
                    # place.get_details()
                    print (place.name)
                    print("Latitude", place.geo_location['lat'])
                    print("Longitude", place.geo_location['lng'])
                    print()

            elif( op2==10):
                break
            else:
                print("Please choose a valid option")



    #Volunteer
    elif (op1==2):
        print("\n \n------------------------------\nWelcome Volunteer")
        while(1):
            print("\n\nChoose the option to proceed")
            print("1. Register and add details \n2. Register with an NGO \n3. Unregister from an NGO \n4. View allotted work \n5. Report completion of work \n6. Update your availability \n7. Go back to main menu")
            op2=int(input("Your Option: "))
            volid = "ll"

            if(op2==1):
                fname=input("Enter first name: ")
                lname=input("Enter last name: ")
                mobile=input("Enter mobile no: ")
                email=input("Enter email id: ")
                house=input("Enter house no: ")
                street=input("Enter street name: ")
                city=input("Enter city name: ")
                state=input("Enter state name: ")
                zip=input("Enter zip: ")
                query =  ''' SELECT * FROM Volunteer;'''
                try:
                    sql_cursor.execute(query)
                    results = sql_cursor.fetchall()
                except Exception as e:
                    print(e)

                number=int((len(results)))
                number+=1
                #print(number)
                number='VOL'+str(number)
                volid = number
                register_volunteer(sql_cursor,volid,fname,lname,mobile,email,house,street,city,state,zip)
                print("Your Volunteer ID is:",number)
            elif (op2==2):
                vid=input("Enter your Volunteer ID: ")
                print("Following is the list of available NGOs: \n")
                query = '''SELECT * FROM NGO;'''
                try:
                    sql_cursor.execute(query)
                    results = sql_cursor.fetchall()
                except Exception as e:
                    print(e)
                pretty_print_results(list(results), sql_cursor.column_names)
                nid=input("Enter the NGO ID you want to be registered with: ")
                reg_volunteer_with_ngo(sql_cursor,vid,nid)
            elif (op2==3):
                vid=input("Enter your Volunteer ID: ")
                print("Select NGO ID for the NGO you want to Unregister from: \n")
                query = '''SELECT NGO_ID FROM Volunteer_NGO WHERE Volunteer_ID = %s and available='yes';'''
                params = [vid]
                try:
                    sql_cursor.execute(query,params)
                    results = sql_cursor.fetchall()
                except Exception as e:
                    print(e)
                pretty_print_results(list(results), sql_cursor.column_names)
                nid = input("\nEnter the NGO ID: ")
                unregister_volunteer(sql_cursor,vid,nid)
            elif (op2==4):
                vid=input("Enter your Volunteer ID: ")
                pretty_print_results(*view_volunteer_work(sql_cursor,vid))
            elif (op2==5):
                vid=input("Enter your Volunteer ID: ")
                print("Select from the allotted services: \n")
                pretty_print_results(*view_volunteer_work(sql_cursor,vid))
                sid = input("Select Service ID: ")
                report_completion_by_volunteer(sql_cursor,vid,sid,time.strftime('%Y%m%d'))
            elif (op2==6):
                vid=input("Enter your Volunteer ID: ")
                update_volunteer_availability(sql_cursor,vid)
            elif(op2==7):
                break
            else:
                print("Please choose a valid option")



    #Government Officer
    elif (op1==4):
        print("\n \n------------------------------\nWelcome NGO")
        while(1):
            print("\n\nChoose the option to proceed")
            print("1. Register NGO")
            print("2. List new Services received from the Government")
            print("3. Allot Services to Volunteers")
            print("4. Display Available Volunteers.")
            print("5. Display number of completed and pending services of a volunteer")
            print("6. Check NGO Transactions within a specified date range")
            print("7. De-Register NGO")
            print("8. Go back to Main Menu")
            op2=int(input("Your Option: "))

            if(op2==1):
                Name = input("Enter NGO name: ")
                Helpline_1 = input("Enter Helpline number 1: ")
                Helpline_2 = input("Enter Helpline number 2: ")
                House_No = input("Enter House No: ")
                Street_Name = input("Enter Street Name: ")
                City = input("Enter City: ")
                State = input("Enter State: ")
                Zip = input("Enter Zip code: ")
                Website = input("Enter Website: ")
                Issue_Type = input("Enter Issue Type of Your NGO: ")
                Service_Cost = input("Enter Service Cost Of your NGO: ")
                register_ngo(mydb, sql_cursor, Name, Helpline_1, Helpline_2, House_No, Street_Name, City, State, Zip, Website, Issue_Type, Service_Cost)
            elif (op2==2):
                ngo_id = input("Enter your NGO ID: ")
                pretty_print_results(*get_services_with_unallotted_volunteers_of_ngo(sql_cursor, ngo_id))
            elif (op2==3):
                ngo_id = input("Enter your NGO ID: ")
                pretty_print_results(*allot_services_to_ngo_volunteers(mydb, sql_cursor, ngo_id))
            elif (op2==4):
                ngo_id = input("Enter your NGO ID: ")
                pretty_print_results(*display_available_volunteers_of_an_ngo(sql_cursor, ngo_id))
            elif (op2==5):
                volunteer_id = input("Enter Volunteer ID: ")
                pretty_print_results(*get_number_of_completed_and_pending_services_volunteer(sql_cursor, volunteer_id))
            elif (op2==6):
                ngo_id = input("Enter your NGO ID: ")
                start_date = input("Enter Starting range date in YYYY-MM-DD format: ")
                end_date = input("Enter Ending range date in YYYY-MM-DD format: ")
                pretty_print_results(*get_ngo_transaction_for_a_date_range(sql_cursor, ngo_id, start_date, end_date))
            elif op2 == 7:
                ngo_id = input("Enter your NGO ID: ")
                deregister_ngo(mydb, sql_cursor, ngo_id)
            elif (op2==8):
                break
            else:
                print("Please choose a valid option")



    #NGO
    elif (op1==4):
        print("\n \n------------------------------\nWelcome NGO")
        while(1):
            print("\n\nChoose the option to proceed")
            print("1. Query 1 \n2. Query 2 \n3. Query 3 \n4. Query 4 \n5. Query 5 \n6. Go back to Main Menu")
            op2=int(input("Your Option: "))

            if(op2==1):
                print("Q1")
            elif (op2==2):
                print("Q2")
            elif (op2==3):
                print("Q3")
            elif (op2==4):
                print("Q4")
            elif (op2==5):
                print("Q5")
            elif (op2==6):
                break
            else:
                print("Please choose a valid option")



    #Family
    elif (op1==5):
        print("\n \n------------------------------\nWelcome Family")
        while(1):
            print("\n\nChoose the option to proceed")
            print("1. Query 1 \n2. Query 2 \n3. Query 3 \n4. Query 4 \n5. Query 5 \n6. Go back to Main Menu")
            op2=int(input("Your Option: "))

            if(op2==1):
                print("Q1")
            elif (op2==2):
                print("Q2")
            elif (op2==3):
                print("Q3")
            elif (op2==4):
                print("Q4")
            elif (op2==5):
                print("Q5")
            elif (op2==6):
                break
            else:
                print("Please choose a valid option")



    #Healthcare Worker
    elif (op1==6):
        print("\n \n------------------------------\nWelcome Healthcare Worker")
        while(1):
            print("\n\nChoose the option to proceed")
            print("1. Query 1 \n2. Query 2 \n3. Query 3 \n4. Query 4 \n5. Query 5 \n6. Go back to Main Menu")
            op2=int(input("Your Option: "))

            if(op2==1):
                print("Q1")
            elif (op2==2):
                print("Q2")
            elif (op2==3):
                print("Q3")
            elif (op2==4):
                print("Q4")
            elif (op2==5):
                print("Q5")
            elif (op2==6):
                break
            else:
                print("Please choose a valid option")




    elif (op1==7):
        print("Goodbye")
        exit()



    else:
        print("Please choose a valid option")

mydb.close()
