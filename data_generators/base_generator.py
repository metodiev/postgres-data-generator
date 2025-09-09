from faker import Faker
import random

fake = Faker()

class BaseGenerator:
    def __init__(self, table_name, schema="public"):
        self.table_name = table_name
        self.schema = schema

    def generate_value(self, column):
        name = column["name"].lower()
        col_type = str(column["type"]).lower()

        if "int" in col_type:
            return random.randint(1, 10000)
        if "char" in col_type or "text" in col_type:
            if "email" in name:
                return fake.unique.email()
            elif "name" in name:
                return fake.name()
            else:
                return fake.word()
        if "date" in col_type:
            return fake.date_this_decade()
        if "bool" in col_type:
            return random.choice([True, False])
        return None
