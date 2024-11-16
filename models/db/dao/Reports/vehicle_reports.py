from models.db.common.database_query import run_db_fetch_query
from models.locations import Locations
from models.db.dao.vehicle_dao import Vehicle


def vehicle_count_total():  # Returns single integer - Total vehicles count
    return len(Vehicle.list_all_vehicles())


def vehicle_count_by_location():
    locations_list = Locations.glasgow_accepted_zip_codes
    zipcodes_list = []
    for loc in locations_list:
        zipcodes_list.append(loc[0])
    print(zipcodes_list)
    zipcode_vehicle_count_dict_list = []
    for i in range(len(zipcodes_list)):
        vehicles_by_loc = Vehicle.list_all_vehicles_by_location(zipcodes_list[i])
        if len(vehicles_by_loc) > 0:
            dict = {'location': zipcodes_list[i], 'count': len(vehicles_by_loc), 'name': locations_list[i][1]}
        else:
            dict = {'location': zipcodes_list[i], 'count': 0, 'name': locations_list[i][1]}
        zipcode_vehicle_count_dict_list.append(dict)
    return zipcode_vehicle_count_dict_list


def vehicle_count_by_type():  # returns a list of tuple ('vehicle_type', count)
    query = """
        SELECT vehicle_type, COUNT(*) FROM vehicle GROUP BY vehicle_type;
    """
    vehicle_row = run_db_fetch_query(query)
    return vehicle_row


def vehicle_active_by_location():
    query = """
        SELECT current_loc, vehicle_type, COUNT(*) FROM vehicle 
        WHERE repair_status = 0 AND available = 1 AND charge > 0.0
        GROUP BY current_loc, vehicle_type;
    """
    vehicle_row = run_db_fetch_query(query)
    return vehicle_row


# group ride table by location for total revenue per location
def vehicle_count_by_type_rented():
    query = """
        SELECT COUNT(*), v.vehicle_type , to_char(start_time::date, 'Day')
        FROM vehicle v INNER JOIN ride r ON v.id = r.vehicle_id 
        WHERE start_time::timestamp >= current_date at time zone 'UTC' - interval '7 days' 
        GROUP BY v.vehicle_type, 3;     
    """
    vehicle_row = run_db_fetch_query(query)
    return vehicle_row


def top_vehicle_count_by_maintainence():
    query = """
        SELECT id, repair_counts FROM vehicle ORDER BY repair_counts DESC LIMIT 10;
    """
    vehicle_row = run_db_fetch_query(query)
    return vehicle_row
