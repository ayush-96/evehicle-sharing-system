from ..common.database_query import run_db_update_query, run_db_fetch_query


class Ride:
    ride_id = None
    vehicle_id = None
    customer_id = None
    start_loc = ""
    end_loc = ""
    start_time = ""
    total_time = 0
    ride_cost = 0.0

    def __init__(
        self,
        ride_id="",
        vehicle_id="",
        customer_id="",
        start_loc="",
        end_loc="",
        start_time="",
        total_time=0,
        ride_cost=0.0,
    ):
        self.ride_id = ride_id
        self.vehicle_id = vehicle_id
        self.customer_id = customer_id
        self.start_loc = start_loc
        self.end_loc = end_loc
        self.start_time = start_time
        self.total_time = total_time
        self.ride_cost = ride_cost

    @staticmethod
    def get_ride_details_by_id(ride_id):
        search_query = "SELECT * FROM ride WHERE ride_id = '{}'".format(ride_id)
        ride_row = run_db_fetch_query(search_query)
        ride_details_list = []
        for detail in ride_row[0]:
            ride_details_list.append(detail)
        return ride_details_list

    @staticmethod
    def get_ride_details_by_vehicle_id_active(vehicle_id):
        search_query = """
            SELECT ride_id FROM ride where vehicle_id = '{}' and end_loc IS NULL;
        """.format(
            vehicle_id
        )
        ride_row = run_db_fetch_query(search_query)
        ride_details_list = []
        for detail in ride_row[0]:
            ride_details_list.append(detail)
        return ride_details_list[0]

    def set_ride_object_details_by_id(self):
        ride_details = self.get_ride_details_by_id(self.ride_id)
        self.vehicle_id, self.customer_id = ride_details[1], ride_details[2]
        self.start_loc = ride_details[3]
        if self.end_loc is None:
            self.end_loc = ride_details[4]
        self.start_time, self.total_time = ride_details[5], ride_details[6]
        self.ride_cost = ride_details[7]
        print("Updated the Ride object values with latest values from database")

    def update_ride_end_loc(self, end_location):
        update_endloc_query = """
            UPDATE ride SET end_loc = '{}' WHERE ride_id = '{}'
        """.format(
            end_location, self.ride_id
        )
        return run_db_update_query(update_endloc_query)

    def update_ride_total_time(self, ride_time):
        update_totaltime_query = """
            UPDATE ride SET total_time = {} WHERE ride_id = '{}'
        """.format(
            ride_time, self.ride_id
        )
        return run_db_update_query(update_totaltime_query)

    def update_ride_ride_cost(self, ride_cost):
        update_ridecost_query = """
            UPDATE ride SET ride_cost = {} WHERE ride_id = '{}'
        """.format(
            ride_cost, self.ride_id
        )
        return run_db_update_query(update_ridecost_query)


# Ride end functionality below
# rideobj = Ride(ride_id='704ae801db', end_loc='G4')
# rideobj.set_ride_object_details_by_id()

# Ride.get_ride_details_by_vehicle_id_active("fedc8765")
