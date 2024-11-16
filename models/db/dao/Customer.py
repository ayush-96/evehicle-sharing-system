import random
from ..common.utils import generate_uuid
from ..common.database_query import (
    run_db_update_query,
    run_db_fetch_query,
    run_db_update_query_params,
)


class Customer:
    customer_id = ""
    password = str(random.randint(1, 10000))
    name = ""
    phone = ""
    dob = ""
    vehicle_id = ""
    total_trips = 0
    total_billing = 0.0
    current_status = False
    payment_dues = 0.0
    report_defective = False

    def __init__(
        self,
        cid=None,
        password=str(random.randint(1, 10000)),
        cname="",
        cphone="",
        cdob="",
        cvehicle_id=None,
        ctotal_trips=0,
        ctotal_billing=0.0,
        ccurrent_status=0,
        cpayment_dues=0.0,
        creport_defective=0,
    ):
        self.customer_id = cid
        self.password = password
        self.name = cname
        self.phone = cphone
        self.dob = cdob
        self.vehicle_id = cvehicle_id
        self.total_trips = ctotal_trips
        self.total_billing = ctotal_billing
        self.current_status = ccurrent_status
        self.payment_dues = cpayment_dues
        self.report_defective = creport_defective

    def create_new_user(self):
        new_customer_id = generate_uuid()
        new_customer_tuple = (
            new_customer_id,
            self.password,
            self.name,
            self.phone,
            self.dob,
            None,
            0,
            0.0,
            0,
            0.0,
            0,
        )
        insert_query = """INSERT INTO customer(customer_id, password, name, phone, dob, vehicle_id, total_trips,
                       total_billing, current_status, payment_dues, report_defective)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        query_result = run_db_update_query_params(insert_query, new_customer_tuple)
        if query_result:
            print("New Customer Registered! User ID : ", new_customer_id)
        return new_customer_id

    @staticmethod
    def get_registered_users_count():
        total_users_query = """
            SELECT COUNT(*) FROM customer;
        """
        customer_details_list = run_db_fetch_query(total_users_query)
        return customer_details_list

    @staticmethod
    def get_active_users_count():
        total_active_users_query = """
                    SELECT COUNT(*) FROM customer WHERE current_status = 1;
                """
        customer_details_list = run_db_fetch_query(total_active_users_query)
        return customer_details_list

    def get_customer_details_by_id(self):
        search_query = "SELECT * FROM customer WHERE customer_id = '{}';".format(
            self.customer_id
        )
        customer_details_list = run_db_fetch_query(search_query)
        try:
            if len(customer_details_list) == 0:
                print("No result found for the query! 0 rows returned")
        except IndexError as e:
            print("Exception occured while getting customer details by id")
        return customer_details_list

    def get_customer_login_details_by_id(self):
        login_query = """
            SELECT customer_id, password FROM customer WHERE customer_id = '{}';
        """.format(
            self.customer_id
        )
        customer_details_list = run_db_fetch_query(login_query)
        try:
            if len(customer_details_list) == 0:
                print("Unable to fetch login details!")
        except IndexError as e:
            return 0
        except Exception as e:
            print("Some exception occured!")
            return -1
        return customer_details_list[0][0], customer_details_list[0][1]

    def set_customer_object_details_by_id(self):
        try:
            customer_details = self.get_customer_details_by_id()[
                0
            ]  # added [0] index as fetching for 1 customer only
            self.password = customer_details[1]
            self.name, self.phone, self.dob = (
                customer_details[2],
                customer_details[3],
                customer_details[4],
            )
            self.vehicle_id, self.total_trips = customer_details[5], customer_details[6]
            self.total_billing, self.current_status = (
                customer_details[7],
                customer_details[8],
            )
            self.payment_dues, self.report_defective = (
                customer_details[9],
                customer_details[10],
            )
            print("Updated the Customer object values with latest values from database")
        except IndexError as e:
            print("Exception occured while setting object values from database")

    def update_customer_current_status(self, status=0):
        update_availability_query = """
            UPDATE customer SET current_status = {} where customer_id = '{}';
        """.format(
            status, self.customer_id
        )
        return run_db_update_query(update_availability_query)

    def update_customer_dob(self, new_dob):
        update_query = "UPDATE customer SET dob = %s WHERE customer_id = %s"
        update_value_tuple = (new_dob, self.customer_id)
        result_flag = run_db_update_query_params(update_query, update_value_tuple)
        result = (
            "Successful date of birth update!"
            if result_flag
            else "Failed to update date of birth!"
        )
        print(result)

    def update_customer_phone(self, new_phone):
        update_query = "UPDATE customer SET phone = %s WHERE customer_id = %s;"
        update_value_tuple = (new_phone, self.customer_id)
        result_flag = run_db_update_query_params(update_query, update_value_tuple)
        result = (
            "Successful phone number update!"
            if result_flag
            else "Failed to update phone number!"
        )
        print(result)

    def update_customer_name(self, new_name):
        update_query = "UPDATE customer SET name = %s WHERE customer_id = %s;"
        update_value_tuple = (new_name, self.customer_id)
        result_flag = run_db_update_query_params(update_query, update_value_tuple)
        result = "Successful name update!" if result_flag else "Failed to update name!"
        print(result)

    def update_customer_vehicle_id(self, rented_vehicle_id):
        update_query = "UPDATE customer SET vehicle_id = %s WHERE customer_id = %s"
        update_value_tuple = (rented_vehicle_id, self.customer_id)
        result_flag = run_db_update_query_params(update_query, update_value_tuple)
        result = (
            "Successful updated rented vehicle id for customer!"
            if result_flag
            else "Failed to update!"
        )
        print(result)

    def update_customer_total_trips(self, count=1):
        update_totaltrips_query = """
                            UPDATE customer SET total_trips=total_trips+1 where customer_id = '{}';
                        """.format(
            self.customer_id
        )
        return run_db_update_query(update_totaltrips_query)

    def update_customer_payment_dues(self, ride_cost):
        update_paymentdues_query = """
                            UPDATE customer SET payment_dues=payment_dues+{} where customer_id = '{}';
                        """.format(
            ride_cost, self.customer_id
        )
        return run_db_update_query(update_paymentdues_query)

    def update_customer_clear_payment_dues(self):
        update_paymentdues_query = """
            UPDATE customer SET payment_dues = 0 where customer_id = '{}';
        """.format(
            self.customer_id
        )
        return run_db_update_query(update_paymentdues_query)

    def update_customer_total_billing(self, ride_cost):
        update_totalbilling_query = """
                            UPDATE customer SET total_billing=total_billing+{} where customer_id = '{}';
                        """.format(
            ride_cost, self.customer_id
        )
        return run_db_update_query(update_totalbilling_query)

    def update_customer_report_defective(self):
        update_reportdefective_query = """
            UPDATE customer SET report_defective=report_defective+1 where customer_id = '{}';
        """.format(
            self.customer_id
        )
        return run_db_update_query(update_reportdefective_query)
