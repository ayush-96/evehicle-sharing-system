from ..common.database_query import run_db_update_query
from ..dao.Customer import Customer
from ..dao.vehicle_dao import Vehicle


def buy_vehicle(vehicle_obj, customer_id):  # Vehicle object, customer id
    vehicle_cost = round((vehicle_obj.cost * 100), 2)  # cost of vehicle -> 100 times the rent

    cust = Customer(customer_id)
    cust.set_customer_object_details_by_id()
    cust.update_customer_payment_dues(vehicle_cost)  # updating customer due payment
    cust.update_customer_total_billing(vehicle_cost)  # updating customer total billing amount

    # Removing the vehicle from the vehicle table
    delete_vehicle_query = """ 
        DELETE FROM vehicle WHERE id = '{}';
    """.format(vehicle_obj.id)

    return run_db_update_query(delete_vehicle_query)
