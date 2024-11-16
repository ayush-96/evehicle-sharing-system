from json import*
import json
from django.shortcuts import render
from django.http import HttpResponseRedirect,JsonResponse
from passlib.hash import pbkdf2_sha256
from models.db.dao.Customer import Customer
from models.db.dao.vehicle_dao import Vehicle
from models.db.dao.Rent import validate_update_customer_table,validate_update_vehicle_table,start_ride_rent
from models.db.dao.ride_dao import Ride
from models.db.dao.Return import end_rent_ride
from models.db.dao.Defective import report_vehicle_defective
from models.db.dao.staff_dao import Staff
from models.db.dao.Reports import vehicle_reports, user_reports, location_reports
from models.db.dao.operator_dao import Operator
from datetime import datetime, timedelta
import calendar
from models.db.dao.buy import*

def index(request):
    return render(request, 'home/index.html')

def about_us(request):
    return render(request, 'home/AboutUs.html')

def UserLogin(request):
    #username= request.POST.get('username')
    #password= request.POST.get('password')
    #print(username, password)
    if request.method == 'POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        print(username, password)
        CustomerLogin= Customer(cid=username)
        CustomerLoginTest= CustomerLogin.get_customer_login_details_by_id()
        print(CustomerLoginTest)
        print(CustomerLoginTest[1])
        print(pbkdf2_sha256.verify("password", CustomerLoginTest[1]))
        #hashPass = Convert.ToBase64String(CustomerLoginTest[1]);
        if pbkdf2_sha256.verify(password, CustomerLoginTest[1]):
            global active_user
            active_user=CustomerLoginTest[0]
            return HttpResponseRedirect('/home/UserHomePage/')
    return render(request, 'home/UserLogin.html')

"""def create_customer_id():
    return (str(uuid.uuid4())[:-5].replace('-', '') +
            str(random.randint(1000, 9999)) +
            str(random.choice(string.ascii_lowercase)))[:10]"""

def hashedpassword(password):
    hashedPassword= pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=12 )
    #print(type(hashedPassword))
    return hashedPassword

def UserRegistration(request):
    print(str(request.method))
    if request.method=="POST":
        name = str(request.POST.get("register-username"))
        password= str(request.POST.get("register-password"))
        hashedpassworddb= str(hashedpassword(password))
        phone = request.POST.get("register-phonenumber")
        dob = request.POST.get("register-dob")
        return_object=str(name)+"\n"+str(password)+"\n"+str(phone)+"\n"+str(dob)+'\n'
        print(return_object)
        print("pass")
        if name and password and phone and dob:
            #return_object=str(name)+"\n"+str(password)+"\n"+str(phone)+"\n"+str(dob)+'\n'
            #print(return_object+"2")
            new_customer = Customer(cid=None, password=hashedpassworddb, cname=name, cphone=phone, cdob=dob)
            new_customer_id_test = new_customer.create_new_user()
            print("ok")
            return render(request, 'home/UserLogin.html', {"cid": new_customer_id_test})
        
    #return_object2=str(name)+"22\n"+password+"\n"+hashedpassworddb+"\n"+phone+"\n"+dob+'\n'+str(pbkdf2_sha256.verify('password', hashedpassworddb))
    #print(return_object2)
    return render(request, 'home/UserRegistration.html')


# c = Customer(None, password="1234", cphone="7064005631", cdob="12-09-1994")
# c.create_new_user()

def UserHomePage(request):
    print("active_user",active_user)
    c_details= Customer(cid=active_user)
    c_details.set_customer_object_details_by_id()
    vid=c_details.vehicle_id
    cname=c_details.name
    dueamt=c_details.payment_dues
    print(dueamt)
    if request.method == "POST":
        location= request.POST.get("location")
        vtype= request.POST.get("vehicle-type")
        print(location, vtype)
        if location and vtype:
            vehicle_check=Vehicle(current_loc= location, vehicle_type=vtype)
            global available_vehicles_at_zip_code_list
            available_vehicles_at_zip_code_list=vehicle_check.list_all_available_vehicles_by_location_vehicle_type(location, vtype)
            print(available_vehicles_at_zip_code_list)
            if len(available_vehicles_at_zip_code_list) == 0:
                result="No vehicle available at {available_vehicles_at_zip_code_list[0][2]}"
            else:
                print(f"{len(available_vehicles_at_zip_code_list)} {available_vehicles_at_zip_code_list[0][1]} available !!! at {available_vehicles_at_zip_code_list[0][2]}")
                result=f"{len(available_vehicles_at_zip_code_list)} {available_vehicles_at_zip_code_list[0][1]} available !!! at {available_vehicles_at_zip_code_list[0][2]}"
            buyv= Vehicle(available_vehicles_at_zip_code_list[0][0])
            buyv.set_vehicle_object_details_by_id()
            price=buyv.cost*100
            print(price)
            return render(request, 'home/UserHomePage.html', {"vehicle_availability": result, 'price':price, "c_name": cname, "due_amount":dueamt})
     
      
        vrent_buy= request.POST.get("user_choice")
        print(vrent_buy)
        if vrent_buy == 'rent':
            #print(validate_update_customer_table(active_user, available_vehicles_at_zip_code_list[0][0]))
            #print(validate_update_vehicle_table(available_vehicles_at_zip_code_list[0][0]))
            #vid=start_ride_rent(available_vehicles_at_zip_code_list[0][0], active_user)
            #print(vid)
            rentv = Vehicle(available_vehicles_at_zip_code_list[0][0])
            rentv.set_vehicle_object_details_by_id()
            price=rentv.cost*100
            print(rentv.id)
            ride_id=rentv.rent_selected_vehicle(active_user)
            return render(request, 'home/UserHomePage.html', {"rvehicle_id": available_vehicles_at_zip_code_list[0][0], "c_name": cname, "due_amount":dueamt, 'price':price})
        elif vrent_buy == 'buy':
            buyv= Vehicle(available_vehicles_at_zip_code_list[0][0])
            buyv.set_vehicle_object_details_by_id()
            price=buyv.cost*100
            print(price)
            buy_vehicle(buyv, active_user)
            due=c_details.payment_dues
            c_details= Customer(cid=active_user)
            c_details.set_customer_object_details_by_id()
            dueamt=c_details.payment_dues
            return render(request, 'home/UserHomePage.html', {"bvehicle_id": available_vehicles_at_zip_code_list[0][0], 'due':due, "c_name": cname, "due_amount":dueamt})
        #vreturn= request.POST.get("return")

        vreturn= request.POST.get("user_choice")
        vloc=request.POST.get("rlocation")
        print(vreturn)
        if vreturn == 'return':
            ride_object = Ride(Ride.get_ride_details_by_vehicle_id_active(vid))
            ride_object.set_ride_object_details_by_id()
            end_rent_ride(ride_object.ride_id, vid, vloc, ride_object.start_time)
            c_details= Customer(cid=active_user)
            c_details.set_customer_object_details_by_id()
            dueamt=c_details.payment_dues
            return render(request, 'home/UserHomePage.html', {"c_name": cname, "due_amount":dueamt})
        
        vstatus= request.POST.get("report_defective")
        print(vstatus)
        print(vid, vloc)
        if vstatus == "report_defective":
            report_vehicle_defective(vid, vloc) 
            c_details= Customer(cid=active_user)
            c_details.set_customer_object_details_by_id()
            dueamt=c_details.payment_dues
            return render(request, 'home/UserHomePage.html', {"c_name": cname, "due_amount":dueamt})  

        damt= request.POST.get("due_amount") 
        if damt == "due_amount":
            c_details.update_customer_clear_payment_dues()
            c_details= Customer(cid=active_user)
            c_details.set_customer_object_details_by_id()
            vid=c_details.vehicle_id
            cname=c_details.name
            dueamt=c_details.payment_dues
            return render(request, 'home/UserHomePage.html', {"c_name": cname, "due_amount":dueamt})  
        
        logout=request.POST.get("logout")
        #print(logout)
        if logout:
            return HttpResponseRedirect("/home/UserLogin/")

    c_details= Customer(cid=active_user)
    c_details.set_customer_object_details_by_id()
    vid=c_details.vehicle_id
    cname=c_details.name
    dueamt=c_details.payment_dues


    return render(request, 'home/UserHomePage.html',{"vehicle_id": vid, "c_name": cname, "due_amount":dueamt})

def stafflogin(request):
    if request.method == 'POST':
        staffUsername= request.POST.get('staffUsername')
        staffPassword= request.POST.get('staffPassword')
        staffRole= request.POST.get('staffRole')

        print(staffPassword, staffPassword, staffRole)
        staff= Staff(employee_id=staffUsername)
        staff.set_staff_object_details_by_id()
        stafflogintest=staff.get_staff_login_details_by_id(employee_type=staffRole)
        print(stafflogintest)
        # print(CustomerLoginTest)
        # print(CustomerLoginTest[1])
        # print(pbkdf2_sha256.verify("password", CustomerLoginTest[1]))
        #hashPass = Convert.ToBase64String(stafflogintest[1]);
        global active_staff
        if staffRole == "manager" and pbkdf2_sha256.verify(staffPassword, stafflogintest[1]):
            active_staff=stafflogintest[0]
            return HttpResponseRedirect("/manager/manager_dashboard/")
        elif staffRole == "operator" and pbkdf2_sha256.verify(staffPassword, stafflogintest[1]):
            active_staff=stafflogintest[0]
            return HttpResponseRedirect("/operator/operator/")
    return render(request, "home/StaffLogin.html")

def operator_page(request):
    vdetails=Vehicle.list_all_vehicles()
    operator=Operator(active_staff)
    operator.set_operator_details_by_id()
    #print(vdetails)
    if request.method == "POST":
        print(request.POST.get("charge"))
        if request.POST.get("charge") and request.POST.getlist("vselect"):
            #if request.POST.get("charge") == 'charge':
            vtoc=request.POST.getlist("vselect")
            print('vtoc', vtoc)
            # operator=Operator(active_staff)
            # operator.set_operator_details_by_id()
            for v in vtoc:
                operator.charge_vehicles(vehicle_id=v)
            return HttpResponseRedirect("/operator/operator/")
        if request.POST.get("repair") and request.POST.getlist("vselect"):
            vtoc=request.POST.getlist("vselect")
            print('vtoc', vtoc)
            # operator=Operator(active_staff)
            # operator.set_operator_details_by_id()
            for v in vtoc:
                operator.repair_vehicles(vehicle_id=v)
            return HttpResponseRedirect("/operator/operator/")
        if request.POST.get("move") and request.POST.get('location') and request.POST.getlist("vselect"):
            vtoc=request.POST.getlist("vselect")
            vloc=request.POST.get('location')
            print('vtoc', vtoc)
            # operator=Operator(active_staff)
            # operator.set_operator_details_by_id()
            for v in vtoc:
                operator.move_vehicle(vehicle_id=v, new_location=vloc)
            return HttpResponseRedirect("/operator/operator/")
        logout=request.POST.get("logout")
            #print(logout)
        if logout:
            return HttpResponseRedirect("/home/StaffLogin/")
        
        
    return render(request, "operator/operator.html", {'vdetails':vdetails, "operator_name":operator.employee_name, 'vehicle_repair':operator.total_vehicles_repaired, "vehicle_moved":operator.total_vehicles_moved, "vehicle_charged":operator.total_vehicle_charged}) 

def manager_dashboard(request):
    #list_all_vehicles_by_location
    ruser=Customer.get_registered_users_count()
    tvehicle=vehicle_reports.vehicle_count_total()
    vehicle_location = vehicle_reports.vehicle_count_by_location()
    #print(vehicle_location)
    location_name=[]
    for vn in range(len(vehicle_location)):
        location_name.append(vehicle_location[vn]['name'])
    #print('location_name', location_name)
    location_nameJSON= dumps(location_name)
    location_count=[]
    for vn in range(len(vehicle_location)):
        location_count.append(vehicle_location[vn]['count'])
    #print('location_count', location_count)
    location_countJSON= dumps(location_count)

    rented_vehicle=vehicle_reports.vehicle_count_by_type_rented()
    print(rented_vehicle)

    
    bike= vehicle_rented_days("bike", rented_vehicle)
    cycle= vehicle_rented_days("cycle", rented_vehicle)
    skateboard=vehicle_rented_days("skateboard", rented_vehicle)
    delivery= vehicle_rented_days("delivery", rented_vehicle)

    #print("rented data", bike, cycle, skateboard, delivery)
    bikeJSON=dumps(bike)
    cycleJSON=dumps(cycle)
    skateboardJSON=dumps(skateboard)
    deliveryJSON=dumps(delivery)

    operator=Operator(active_staff)
    operator.set_operator_details_by_id()
    if request.method == "POST":
        logout=request.POST.get("logout")
            #print(logout)
        if logout:
            return HttpResponseRedirect("/home/StaffLogin/")


    return render(request, "manager/manager_dashboard.html", {"ruser":ruser[0][0], "tvehicle":tvehicle, "location_name":location_nameJSON, "location_count":location_countJSON, "manager_name":operator.employee_name, "bike":bikeJSON, "cycle":cycleJSON, "skateboard":skateboardJSON, "delivery":deliveryJSON} )

def vehicle_rented_days(vtype, vdata):
    vehicle=[0,0,0,0,0,0,0]
    #print(data[1] == vtype,data[2].strip() )
    for data in vdata:
        if data[1] == vtype and data[2].strip()== "Monday":
                #print('data', data[0])
                vehicle[0] = data[0]
        elif data[1] == vtype and data[2].strip()== "Tuesday":
                vehicle[1] = data[0]
        elif data[1] == vtype and data[2].strip()== "Wednesday":
                vehicle[2] = data[0]
        elif data[1] == vtype and data[2].strip()== "Thursday":
                vehicle[3] = data[0]
        elif data[1] == vtype and data[2].strip()== "Friday":
                vehicle[4] = data[0]
        elif data[1] == vtype and data[2].strip()== "Saturday":
                vehicle[5] = data[0]
        elif data[1] == vtype and data[2].strip()== "Sunday":
                vehicle[6] = data[0]
        else:
            pass
    return vehicle
         
    

def get_user_id_and_data(ltdata):
    uid, data=[], []
    for users in ltdata:
        uid.append(users[0])
        data.append(users[1])
    return uid, data

def manager_userpage(request):
    
    top_users_revenue=user_reports.top_users_revenue()
    # print(top_users_revenue)
    uid, revenue=get_user_id_and_data(top_users_revenue)
    uidJSON= dumps(uid)
    revenueJSON= dumps(revenue)

    top_users_total_trips=user_reports.top_users_total_trips()
    print(top_users_total_trips)
    tuid, trips=get_user_id_and_data(top_users_total_trips)
    tuidJSON= dumps(tuid)
    tripsJSON= dumps(trips)

    top_users_total_trips=user_reports.top_users_reported_defective()
    print(top_users_total_trips)
    duid, defective=get_user_id_and_data(top_users_total_trips)
    duidJSON= dumps(duid)
    defectiveJSON= dumps(defective)

    
    top_users_payment_dues=user_reports.top_users_payment_dues()
    print('payment',top_users_payment_dues)
    puid, due=get_user_id_and_data(top_users_payment_dues)
    duidJSON= dumps(puid)
    defectiveJSON= dumps(due)

    operator=Operator(active_staff)
    operator.set_operator_details_by_id()

    

    return render(request, "manager/User.html", {"uid":uidJSON, 'revenue':revenueJSON, "tuid":tuidJSON, 'trips':tripsJSON, "duid":duidJSON, 'defective':defectiveJSON, "puid":duidJSON, 'due':defectiveJSON, "manager_name":operator.employee_name})

def manager_locationpage(request):
    car_per_location_data=location_reports.count_cars_per_location()
    print(car_per_location_data)
    location=[]
    car_count=[]
    for car_data in car_per_location_data:
        location.append(car_data[1])
        car_count.append(car_data[0])
    locationJSON=dumps(location)
    car_countJSON=dumps(car_count)

    rlocation=[]
    lrevenue=[]
    location_revenue=location_reports.revenue_by_location()
    print(location_revenue)
    for loc in location_revenue:
        rlocation.append(loc[1])
        lrevenue.append(loc[0])
    rlocationJSON=dumps(rlocation)
    lrevenueJSON=dumps(lrevenue)

    operator=Operator(active_staff)
    operator.set_operator_details_by_id()

    return render(request, "manager/Location.html", {"location":locationJSON, "car_count":car_countJSON, 'rlocation':rlocationJSON, 'lrevenue':lrevenueJSON, "manager_name":operator.employee_name})

def manager_vehiclepage(request):
    vehicle_count = vehicle_reports.vehicle_count_by_type()
    print(vehicle_count)
    vehicle_type_count=[]
    for vn in range(len(vehicle_count)):
        print(vn,vehicle_count[vn][0])
        vehicle_type_count.append(vehicle_count[vn][0])
    print('vehicle_type_count', vehicle_type_count)
    vehicle_type_countJSON= dumps(vehicle_type_count)
    vehicle_type_counts=[]
    for vn in range(len(vehicle_count)):
        vehicle_type_counts.append(vehicle_count[vn][1])
    print('vehicle_type_counts', vehicle_type_counts)
    vehicle_type_countsJSON= dumps(vehicle_type_counts)

    active_vehicle_data=vehicle_reports.vehicle_active_by_location()
    print(active_vehicle_data)
    location=[]
    vehicle=[]
    for vehicle in active_vehicle_data:
         location.append(vehicle[0])
    vbike=[0]*len(location)
    vcycle=[0]*len(location)
    vskateboard=[0]*len(location)
    vdelivery=[0]*len(location)
    for vehicle in active_vehicle_data:
        lbike=active_veh_loc_type('bike', location, vehicle, vbike)
        lcycle=active_veh_loc_type('cycle', location, vehicle, vcycle)
        lskateboard=active_veh_loc_type('skateboard', location, vehicle, vskateboard)
        ldelivery=active_veh_loc_type('delivery', location, vehicle, vdelivery)
    print(lbike, lcycle, lskateboard, ldelivery)
    lbikeJSON=dumps(lbike)
    lcycleJSON=dumps(lcycle)
    lskateboardJSON=dumps(lskateboard)
    ldeliveryJSON=dumps(ldelivery)
    llocation=dumps(location)


    damage_vehicle_data = vehicle_reports.top_vehicle_count_by_maintainence()
    print(damage_vehicle_data)
    vid=[]
    damage_count=[]
    for vehicle in damage_vehicle_data:
        vid.append(vehicle[0])
        damage_count.append(vehicle[1])

    vidJSON=dumps(vid)
    damage_countJSON=dumps(damage_count)

    operator=Operator(active_staff)
    operator.set_operator_details_by_id()
    

    return render(request, "manager/Vehicles.html", {"vehicle_type_count":vehicle_type_countJSON, "vehicle_type_counts":vehicle_type_countsJSON, 'location':llocation, 'bike':lbikeJSON, 'cycle':lcycleJSON, 'skateboard':lskateboardJSON, 'delivery':ldeliveryJSON, 'vid':vidJSON, 'damage_count':damage_countJSON, "manager_name":operator.employee_name})

def active_veh_loc_type(vtype, location, vehicle, vlocation):
    for i in range(len(location)):
        print(vehicle[0],location[i], vehicle[1], vtype, vehicle[0] == location[i] , vehicle[1] == vtype)
        if vehicle[0] == location[i] and vehicle[1] == vtype:
            vlocation[i]= vehicle[2]
            #print(vlocation)
    #print("function inside: " , vlocation)
    return vlocation

def Settings(request):
    return render(request, "home/Settings.html")

def Privacy(request):
    return render(request, "home/Privacy.html")

def Notifications(request):
    return render(request, "home/Notifications.html")