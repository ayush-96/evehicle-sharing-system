from ..dao.Return import end_rent_ride
from ..dao.Customer import Customer
from ..dao.ride_dao import Ride
from ..dao.vehicle_dao import Vehicle


def report_vehicle_defective(vehicle_id, defect_loc):
    ride_id = Ride.get_ride_details_by_vehicle_id_active(vehicle_id)
    ride_obj = Ride(ride_id=ride_id, end_loc=defect_loc)
    ride_obj.set_ride_object_details_by_id()
    end_rent_ride(
        ride_obj.ride_id, ride_obj.vehicle_id, ride_obj.end_loc, ride_obj.start_time
    )

    vehicle_obj = Vehicle(vehicle_id)
    vehicle_obj.set_vehicle_object_details_by_id()
    vehicle_obj.update_vehicle_repair_status(1)
    vehicle_obj.update_vehicle_availability()
    vehicle_obj.update_vehicle_repair_counts()

    cust_obj = Customer(ride_obj.customer_id)
    cust_obj.set_customer_object_details_by_id()
    cust_obj.update_customer_report_defective()
