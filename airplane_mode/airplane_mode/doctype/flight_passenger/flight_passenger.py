# Copyright (c) 2024, indrajeet and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class FlightPassenger(Document):
    def validate(self):
        # Automatically set the Full Name before saving the document
        if self.first_name and self.last_name:
            self.full_name = f"{self.first_name} {self.last_name}"
        elif self.first_name:  # If Last Name is missing
            self.full_name = self.first_name
        elif self.last_name:  # If First Name is missing
            self.full_name = self.last_name