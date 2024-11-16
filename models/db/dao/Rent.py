from datetime import datetime
from ..common.database_query import run_db_update_query, run_db_update_query_params
from ..common.utils import generate_uuid
from ..dao.Customer import Customer


def validate_update_customer_table(customer_id, vehicle_id):
    customer_update_flag = False
    customer_obj = Customer(customer_id)
    customer_obj.set_customer_object_details_by_id()

    # Basic validations for customer table before updating table entries
    if (
        customer_obj.current_status == 0
    ):  # Check if customer has a active ride - 1 means riding
        if customer_obj.vehicle_id is None:
            customer_update_flag = True
            customer_obj.update_customer_current_status(
                1
            )  # 1 is for 1 active ride - In future for multiple rides
            customer_obj.update_customer_vehicle_id(vehicle_id)
        else:
            print(
                "Customer still has an active vehicle in possession : ",
                customer_obj.vehicle_id,
            )
    else:
        print("Customer already has an active ride!")
    return customer_update_flag


def validate_update_vehicle_table(vehicle_obj):
    vehicle_update_flag = False

    # Basic validations for customer table before updating table entries
    if (
        vehicle_obj.available == 1
    ):  # Check if vehicle is available. Should be as per drop down list
        if (
            vehicle_obj.charge > 0
        ):  # Check if vehicle is charge. Should be as per drop down list
            if (
                vehicle_obj.repair_status == 0
            ):  # Check if vehicle does not need repair. Should be fine as per list
                vehicle_update_flag = True
                vehicle_obj.update_vehicle_availability(False)
            else:
                print("Vehicle needs repair!")
        else:
            print("Vehicle is not charged : ", vehicle_obj.charge)
    else:
        print(
            "Vehicle is not available! This line should not be printing. Check db!"
        )  # shouldn't be in dropdown list
    return vehicle_update_flag


def start_ride_rent(vehicle_obj, customer_id):
    ride_id = generate_uuid()
    update_query = """INSERT INTO ride(ride_id, vehicle_id, customer_id, 
                    start_loc, end_loc, start_time, total_time, ride_cost)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"""
    update_query_value_tuple = (
        ride_id,
        vehicle_obj.id,
        customer_id,
        vehicle_obj.current_loc,
        None,
        datetime.now(),
        None,
        None,
    )
    query_result_flag = run_db_update_query_params(
        update_query, update_query_value_tuple
    )
    if query_result_flag:
        print("Ride rented! ride id :", ride_id)
    else:
        print("Failed to rent the vehicle")
    return ride_id
