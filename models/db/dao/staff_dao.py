from ..common.database_query import run_db_fetch_query


class Staff:
    employee_id = ""
    password = ""
    employee_name = ""
    employee_phone = ""
    tenure = ""
    employee_type = ""

    def __init__(
        self,
        employee_id=None,
        password=None,
        employee_name=None,
        employee_phone="",
        tenure="",
        employee_type="",
    ):
        # Instance variables
        self.employee_id = employee_id
        self.password = password
        self.employee_name = employee_name
        self.employee_phone = employee_phone
        self.tenure = tenure
        self.employee_type = employee_type

    def get_staff_details_by_id(self):
        search_query = "SELECT * FROM staff WHERE employee_id = '{}'".format(
            self.employee_id
        )
        employee_details_list = run_db_fetch_query(search_query)
        try:
            if len(employee_details_list) == 0:
                print("No result found for the query! 0 rows returned")
        except IndexError as e:
            print("Exception occured while getting customer details by id")
        return employee_details_list

    def get_staff_login_details_by_id(self, employee_type):
        if self.employee_type != employee_type:
            print("You cannot login as this type of user. Select correct staff type!")
            return -1
        else:
            login_query = """
                SELECT employee_id, password FROM staff WHERE employee_id = '{}';
            """.format(self.employee_id)
            employee_details_list = run_db_fetch_query(login_query)
            try:
                if len(employee_details_list) == 0:
                    print("Unable to fetch login details!")
            except IndexError as e:
                return 0
            except Exception as e:
                print("Some exception occured!")
                return -1
            return employee_details_list[0][0], employee_details_list[0][1]

    def set_staff_object_details_by_id(self):
        staff_details = None
        try:
            staff_details = self.get_staff_details_by_id()[
                0
            ]  # added [0] index as fetching for 1 customer only
            self.password = staff_details[1]
            self.employee_name, self.employee_phone, self.tenure = (
                staff_details[2],
                staff_details[3],
                staff_details[4],
            )
            self.employee_type = staff_details[5]
            print("Updated the Staff object values with latest values from database")
        except IndexError as e:
            print("Exception occured while setting object values from database")
        return staff_details

    @staticmethod
    def get_all_managers():
        all_managers_query = """
            SELECT * FROM staff WHERE employee_type = "manager";
        """
        managers_details_list = run_db_fetch_query(all_managers_query)
        try:
            if len(managers_details_list) == 0:
                print("No result found for the query! 0 rows returned")
        except IndexError as e:
            print("Exception occured while getting customer details by id")
        return managers_details_list

    @staticmethod
    def get_all_operators():
        all_operators_query = """
            SELECT * FROM staff WHERE employee_type = "operator";
        """
        operators_details_list = run_db_fetch_query(all_operators_query)
        try:
            if len(operators_details_list) == 0:
                print("No result found for the query! 0 rows returned")
        except IndexError as e:
            print("Exception occured while getting customer details by id")
        return operators_details_list


# s = Staff(employee_id="EMP005")
# print("Here Staff class : ", s.set_staff_object_details_by_id())
# print(s.get_staff_details_by_id())
# print(Staff.get_all_operators())
