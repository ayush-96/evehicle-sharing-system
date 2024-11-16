from ..common.database_query import run_db_update_query, run_db_fetch_query
from ..dao.Rent import (
    start_ride_rent,
    validate_update_vehicle_table,
    validate_update_customer_table,
)


class Vehicle:
    id = ""
    vehicle_type = ""
    current_loc = ""
    charge = 0.0
    repair_status = 0
    available = 1
    cost = 0.0
    total_ride_time = 0
    ride_counts = 0
    repair_counts = 0

    def __init__(
            self,
            id="",
            vehicle_type="",
            current_loc="",
            charge=0.0,
            repair_status=0,
            available=1,
            cost=0.0,
            total_ride_time=0,
            ride_counts=0,
            repair_counts=0,
    ):
        self.id = id
        self.vehicle_type = vehicle_type
        self.current_loc = current_loc
        self.charge = charge
        self.repair_status = repair_status
        self.available = available
        self.cost = cost
        self.total_ride_time = total_ride_time
        self.ride_counts = ride_counts
        self.repair_counts = repair_counts

    def get_vehicle_details_by_id(self):
        search_query = "SELECT * FROM vehicle WHERE id = '{}'".format(self.id)
        vehicle_row = run_db_fetch_query(search_query)
        vehicles_details_list = []
        for detail in vehicle_row[0]:
            vehicles_details_list.append(detail)
        return vehicles_details_list

    def set_vehicle_object_details_by_id(self):
        vehicles_details = self.get_vehicle_details_by_id()
        self.vehicle_type, self.current_loc = vehicles_details[1], vehicles_details[2]
        self.charge, self.repair_status = vehicles_details[3], vehicles_details[4]
        self.available, self.cost = vehicles_details[5], vehicles_details[6]
        self.total_ride_time, self.ride_counts = (
            vehicles_details[7],
            vehicles_details[8],
        )
        self.repair_counts = vehicles_details[9]
        print("Updated the Vehicle object values with latest values from database")

    @staticmethod
    def list_all_vehicles():
        search_query = """
            SELECT id, vehicle_type, current_loc, charge, repair_status, available,
            cost, total_ride_time, ride_counts, repair_status FROM vehicle ORDER BY current_loc;
        """
        all_vehicles_details_list = run_db_fetch_query(search_query)
        if len(all_vehicles_details_list):
            vehicle_dict_list = []
            for vehicle in all_vehicles_details_list:
                vehicle_dict = {'id': vehicle[0], 'vehicle_type': vehicle[1], 'current_loc': vehicle[2],
                                'charge': vehicle[3], 'repair_status': vehicle[4], 'available': vehicle[5],
                                'cost': vehicle[6], 'total_ride_time': vehicle[7], 'ride_counts': vehicle[8],
                                'repair_counts': vehicle[9]}
                vehicle_dict_list.append(vehicle_dict)
        return vehicle_dict_list

    @staticmethod
    def list_all_vehicles_by_location(
            location_zip_code,
    ):  # Function overloading - zipcode
        search_query = """ SELECT id, vehicle_type, current_loc, charge, repair_status, available, cost, 
                       total_ride_time, ride_counts, repair_status FROM vehicle
                       WHERE current_loc = '{}' ORDER BY current_loc;""".format(
            location_zip_code
        )
        vehicles_at_zip_code_list = run_db_fetch_query(search_query)
        if len(vehicles_at_zip_code_list) == 0:
            print("No Vehicles found at location! Returning empty list")
        return vehicles_at_zip_code_list

    @staticmethod
    def list_all_available_vehicles_by_location(location_zip_code):
        search_query = """ SELECT id, vehicle_type, current_loc, charge, repair_status, available, cost, 
                           total_ride_time, ride_counts, repair_status FROM vehicle
                           WHERE current_loc = '{}' AND available = 1 and charge > 0
                           and repair_status = 0 ORDER BY current_loc; """.format(
            location_zip_code
        )
        available_vehicles_at_zip_code_list = run_db_fetch_query(search_query)
        if len(available_vehicles_at_zip_code_list) == 0:
            print("No available vehicles found at location! Returning empty list")
        return available_vehicles_at_zip_code_list

    @staticmethod
    def list_all_available_vehicles_by_location_vehicle_type(
            location_zip_code, vehicle_type
    ):
        search_query = """ SELECT id, vehicle_type, current_loc, charge, repair_status, available, cost, 
                           total_ride_time, ride_counts, repair_status FROM vehicle
                           WHERE current_loc = '{}' and vehicle_type = '{}' AND available = 1 and charge > 0
                           and repair_status = 0 ORDER BY current_loc; """.format(
            location_zip_code, vehicle_type
        )
        available_vehicles_at_zip_code_list = run_db_fetch_query(search_query)
        if len(available_vehicles_at_zip_code_list) == 0:
            print("No available vehicles found at location! Returning empty list")
        return available_vehicles_at_zip_code_list

    @staticmethod
    def list_all_uncharged_vechicles():
        search_query = """ SELECT id, vehicle_type, current_loc, charge, repair_status, available, cost, 
                                   total_ride_time, ride_counts, repair_status FROM vehicle
                                   WHERE charge = 0 ORDER BY current_loc; """
        all_uncharged_vehicles_list = run_db_fetch_query(search_query)
        if len(all_uncharged_vehicles_list) == 0:
            print(
                "All vehicles seems to be charged! Great job company or no vehicles in use (Not great job)"
            )
        return all_uncharged_vehicles_list

    @staticmethod
    def list_all_uncharged_vechicles_by_location(zipcode):
        search_query = """ SELECT id, vehicle_type, current_loc, charge, repair_status, available, cost, 
                                       total_ride_time, ride_counts, repair_status FROM vehicle
                                       WHERE charge = 0 AND current_loc = '{}' ORDER BY current_loc; """.format(
            zipcode
        )
        all_uncharged_vehicles_list = run_db_fetch_query(search_query)
        if len(all_uncharged_vehicles_list) == 0:
            print("No uncharged vehicles at location : {}".format(zipcode))
        return all_uncharged_vehicles_list

    @staticmethod
    def list_all_damaged_vehicles():
        search_query = """ SELECT id, vehicle_type, current_loc, charge, repair_status, available, cost, 
                                           total_ride_time, ride_counts, repair_status FROM vehicle
                                           WHERE repair_status = 1 ORDER BY current_loc; """
        all_damaged_vehicles_list = run_db_fetch_query(search_query)
        if len(all_damaged_vehicles_list) == 0:
            print("All vehicles seems to be repaired! Great job company")
        return all_damaged_vehicles_list

    @staticmethod
    def list_all_damaged_vechicles_by_location(zipcode):
        search_query = """ SELECT id, vehicle_type, current_loc, charge, repair_status, available, cost, 
                                           total_ride_time, ride_counts, repair_status FROM vehicle
                                           WHERE repair_status = 1 AND current_loc = '{}'; """.format(
            zipcode
        )
        all_damaged_vehicles_list = run_db_fetch_query(search_query)
        if len(all_damaged_vehicles_list) == 0:
            print("No damaged vehicles at location : {}".format(zipcode))
        return all_damaged_vehicles_list

    def update_vehicle_availability(self, availability=False):
        if not availability:
            availability = 0
        else:
            availability = 1
        update_availability_query = """
            UPDATE vehicle SET available = {} where id = '{}';
        """.format(
            availability, self.id
        )
        return run_db_update_query(update_availability_query)

    def rent_selected_vehicle(self, customer_id):
        print("Vehicle requested to be rented : ", self.id)
        customer_update_flag, vehicle_update_flag = False, False
        # Add some checks to ensure only proper vehicles are rentable(double check) and user is not currently active
        # All checks queries -> Rent.py
        customer_update_flag = validate_update_customer_table(customer_id, self.id)
        if customer_update_flag:
            vehicle_update_flag = validate_update_vehicle_table(self)
        ride_id = None
        query_result_flag = self.update_vehicle_availability(False)
        if query_result_flag & customer_update_flag & vehicle_update_flag:
            ride_id = start_ride_rent(self, customer_id)
        return ride_id

    @staticmethod
    def charge_vehicles(vehicle_list):
        if len(vehicle_list) == 1:
            print("Vehicle to be charged: ", vehicle_list[0])
            charge_query = """
                UPDATE vehicle SET charge = 100.0 where id = '{}';
            """.format(
                vehicle_list[0]
            )
        elif len(vehicle_list) > 0:
            uncharged_vehicle_id = []
            for vehicle in vehicle_list:
                uncharged_vehicle_id.append(vehicle[0])
            uncharged_vehicle_id_string = '", "'.join(uncharged_vehicle_id)
            uncharged_vehicle_id_string = '"' + uncharged_vehicle_id_string + '"'
            charge_query = """
                UPDATE vehicle SET charge = 100.0 WHERE id IN ({});
            """.format(
                uncharged_vehicle_id_string
            )
        else:
            print("Wrong choice for charging vehicles!")
            charge_query = """
                SELECT 1 FROM vehicle;
            """
        charge_query_flag = run_db_update_query(charge_query)
        return charge_query_flag

    @staticmethod
    def repair_vehicles(vehicle_list):
        if len(vehicle_list) == 1:
            repair_query = """
                    UPDATE vehicle SET repair_status = 0, available = 1
                     where id = '{}';
                """.format(
                vehicle_list[0]
            )
            vehicle_object = Vehicle(vehicle_list[0])
            vehicle_object.update_vehicle_repair_counts()
        elif len(vehicle_list) > 0:
            repair_vehicle_id = []
            for vehicle in vehicle_list:
                repair_vehicle_id.append(vehicle[0])
                vehicle_object = Vehicle(vehicle[0])
                vehicle_object.update_vehicle_repair_counts()
            repair_vehicle_id_string = '", "'.join(repair_vehicle_id)
            repair_vehicle_id_string = '"' + repair_vehicle_id_string + '"'
            repair_query = """
                    UPDATE vehicle SET repair_status = 0, available = 1
                     WHERE id IN ({});
                """.format(
                repair_vehicle_id_string
            )
        else:
            print("Wrong choice for repairing vehicles!")
            repair_query = """
                    SELECT 1 FROM vehicle;
                """
        repair_query_flag = run_db_update_query(repair_query)
        return repair_query_flag

    def update_vehicle_current_loc(self, location):
        update_currentloc_query = """
                    UPDATE vehicle SET current_loc = '{}' where id = '{}';
                """.format(
            location, self.id
        )
        return run_db_update_query(update_currentloc_query)

    def update_vehicle_ride_count(self, count=1):
        update_ridecount_query = """
                            UPDATE vehicle SET ride_counts = ride_counts+1 where id = '{}';
                        """.format(
            self.id
        )
        return run_db_update_query(update_ridecount_query)

    def update_vehicle_total_ride_time(self, ride_time):
        update_totalridetime_query = """
                            UPDATE vehicle SET total_ride_time = total_ride_time+{} where id = '{}';
                        """.format(
            ride_time, self.id
        )
        return run_db_update_query(update_totalridetime_query)

    def update_vehicle_charge(self, ride_time):
        new_charge = self.charge-(ride_time * 0.3)
        update_charge_query = """
                                UPDATE vehicle SET charge = ROUND({}, 2) where id = '{}';
                            """.format(new_charge, self.id)
        return run_db_update_query(update_charge_query)

    def update_vehicle_repair_status(self, status=0):
        update_repairstatus_query = """
            UPDATE vehicle SET repair_status = 1 where id = '{}';
        """.format(
            self.id
        )
        return run_db_update_query(update_repairstatus_query)

    def update_vehicle_repair_counts(self):
        update_repaircounts_query = """
                            UPDATE vehicle SET repair_counts=repair_counts+1 where id = '{}';
                        """.format(
            self.id
        )
        return run_db_update_query(update_repaircounts_query)
