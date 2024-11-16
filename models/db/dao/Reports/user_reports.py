from models.db.common.database_query import run_db_fetch_query


def top_users_revenue():
    query = """
        SELECT customer_id, total_billing 
        FROM customer
        ORDER BY total_billing DESC
        LIMIT 10;
    """
    user_row = run_db_fetch_query(query)
    return user_row


def top_users_total_trips():
    query = """
        SELECT customer_id, total_trips 
        FROM customer
        ORDER BY total_trips DESC
        LIMIT 10;
    """
    user_row = run_db_fetch_query(query)
    return user_row


def top_users_reported_defective():
    query = """
        SELECT customer_id, report_defective 
        FROM customer
        ORDER BY report_defective DESC
        LIMIT 10;
    """
    user_row = run_db_fetch_query(query)
    return user_row


def top_users_payment_dues():
    query = """
        SELECT customer_id, payment_dues 
        FROM customer
        ORDER BY payment_dues DESC
        LIMIT 10;
    """
    user_row = run_db_fetch_query(query)
    return user_row


def current_active_users():
    query = """
        SELECT c.customer_id, c.name, v.vehicle_type 
        FROM customer c INNER JOIN vehicle v ON c.vehicle_id = v.id
        WHERE c.current_status = 1;
    """
    user_row = run_db_fetch_query(query)
    return user_row
