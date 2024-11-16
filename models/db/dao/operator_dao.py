from ..common.database_query import run_db_update_query
from ..dao.staff_dao import Staff
from ..dao.vehicle_dao import Vehicle


class Operator(Staff):
    employee_id = None
    total_vehicles_repaird = 0
    total_vehicles_moved = 0
    total_vehicle_charged = 0

    def __init__(
        self,
        employee_id=None,
        total_vehicles_repaired=0,
        total_vehicles_moved=0,
        total_vehicle_charged=0,
    ):
        self.employee_id = employee_id
        super().__init__(employee_id=self.employee_id)
        self.total_vehicles_repaired = total_vehicles_repaired
        self.total_vehicles_moved = total_vehicles_moved
        self.total_vehicle_charged = total_vehicle_charged

    @staticmethod
    def track_all_vehicles(zipcode=None):
        try:
            if zipcode is None:
                vehicles = Vehicle.list_all_vehicles()
            else:
                vehicles = Vehicle.list_all_vehicles_by_location(zipcode)
        except IndexError as e:
            print("Nothing in db! how can that be?!")
        return vehicles

    def set_operator_details_by_id(self):
        operator_details = self.set_staff_object_details_by_id()
        self.total_vehicles_repaired = operator_details[6]
        self.total_vehicles_moved = operator_details[7]
        self.total_vehicle_charged = operator_details[8]

    def update_operator_total_vehicles_charged_status(self):
        update_vehicles_charged_query = """
            UPDATE staff SET total_vehicle_charged = total_vehicle_charged+1
            WHERE employee_id = '{}'
        """.format(
            self.employee_id
        )
        run_db_update_query(update_vehicles_charged_query)

    def update_operator_total_vehicles_repaired_status(self):
        update_vehicles_repaired_query = """
            UPDATE staff SET total_vehicles_repaired = total_vehicles_repaired+1
            WHERE employee_id = '{}'
        """.format(
            self.employee_id
        )
        run_db_update_query(update_vehicles_repaired_query)

    def update_operator_total_vehicles_moved_status(self):
        update_vehicles_moved_query = """
            UPDATE staff SET total_vehicles_moved = total_vehicles_moved+1
            WHERE employee_id = '{}'
        """.format(
            self.employee_id
        )
        run_db_update_query(update_vehicles_moved_query)

    def charge_vehicles(self, vehicle_id=None):
        uncharged_vehicle_list = []
        try:
            if vehicle_id is None:
                uncharged_vehicle_list = Vehicle.list_all_uncharged_vechicles()
            else:
                uncharged_vehicle_list.append(vehicle_id)
        except IndexError as e:
            print("Some exceptions occured while fetching uncharged vehicles!")

        if len(uncharged_vehicle_list) == 0:
            print("All vehicles are charged!")
        else:
            flag = Vehicle.charge_vehicles(uncharged_vehicle_list)
            if flag:
                print("Vehicles charged")
                self.update_operator_total_vehicles_charged_status()
            else:
                print("Failed to charge the vehicles!")
        return True

    def repair_vehicles(self, vehicle_id=None):
        repair_vehicle_list = []
        try:
            if vehicle_id is None:
                repair_vehicle_list = Vehicle.list_all_damaged_vehicles()
            else:
                repair_vehicle_list.append(vehicle_id)
        except IndexError as e:
            print("Some exceptions occured while fetching damaged vehicles!")

        if len(repair_vehicle_list) == 0:
            print("All vehicles are repaired! No damage")
        else:
            flag = Vehicle.repair_vehicles(repair_vehicle_list)
            if flag:
                print("Vehicles repaired")
                self.update_operator_total_vehicles_repaired_status()
            else:
                print("Failed to repair the vehicles!")
        return True

    def move_vehicle(self, vehicle_id=None, new_location=None):
        vehicle_obj = Vehicle(vehicle_id)
        if new_location == vehicle_obj.current_loc:
            print("Final destination is same as current location")
        else:
            if vehicle_obj.update_vehicle_current_loc(new_location):
                self.update_operator_total_vehicles_moved_status()
        return True


# o = Operator(employee_id="EMP004")
# o.set_operator_details_by_id()
# o.repair_vehicles()
# o.charge_vehicles(zipcode="G5")
# o.move_vehicle(o.track_all_vehicles()[0][0], "G2")  # Just getting a vehicle and moving it to new location
