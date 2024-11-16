from ..common.utils import get_time_difference
from ..dao.Customer import Customer
from ..dao.ride_dao import Ride
from ..dao.vehicle_dao import Vehicle


def end_rent_ride(ride_id, vehicle_id, end_loc, start_time):
    # Creating Vehicle object and setting attribute values from database
    vehicle_rented = Vehicle(vehicle_id)
    vehicle_rented.set_vehicle_object_details_by_id()
    vehicle_rented.update_vehicle_availability(True)
    vehicle_rented.update_vehicle_current_loc(end_loc)
    vehicle_rented.update_vehicle_ride_count()
    # TODO Something about the charge ---> DONE!

    total_time = round(get_time_difference(start_time) / 60) * 10  # scaling up time difference by 10 (!realtime)
    ride_cost = round((total_time / 5) * vehicle_rented.cost, 2)  # cost is per 5 minutes -> vehicles table
    # Updating Ride table with details after ride end
    ride_obj = Ride(ride_id)
    ride_obj.set_ride_object_details_by_id()
    ride_obj.update_ride_end_loc(end_loc)
    ride_obj.update_ride_total_time(total_time)
    ride_obj.update_ride_ride_cost(ride_cost)

    vehicle_rented.update_vehicle_total_ride_time(total_time)
    vehicle_rented.update_vehicle_charge(total_time)

    customer_obj = Customer(ride_obj.customer_id)
    customer_obj.set_customer_object_details_by_id()
    customer_obj.update_customer_vehicle_id(None)
    customer_obj.update_customer_current_status(0)
    customer_obj.update_customer_total_trips()
    customer_obj.update_customer_payment_dues(ride_cost)
    customer_obj.update_customer_total_billing(ride_cost)

    # Creating Customer object and setting attribute values from database - checking if id's match
    # if customer_id == ride_obj.customer_id:
    #     customer_details = Customer(customer_id)
    #     customer_details.set_customer_object_details_by_id()
    #     vehicle_rented.update_vehicle_availability(True)
    # else:
    #     print("Customer id does not match with Ride table id!")


# end_rent_ride("104acd3f83", "ccb65498", "G12", "2024-10-22 15:18:39.899234")
