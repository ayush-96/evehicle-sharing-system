from models.db.common.database_query import run_db_fetch_query


def count_cars_per_location():
    report_query = """
            SELECT COUNT(*) AS Vehicles, current_loc AS Location
            FROM vehicle
            GROUP BY current_loc
            ORDER BY 1 DESC;
        """
    count_cars_by_location_list = run_db_fetch_query(report_query)
    return count_cars_by_location_list


def revenue_by_location():
    query = """
        SELECT SUM(ride_cost) as total_revenue, start_loc
        FROM ride
        GROUP BY start_loc;
    """
    rev_by_location_list = run_db_fetch_query(query)
    return rev_by_location_list
