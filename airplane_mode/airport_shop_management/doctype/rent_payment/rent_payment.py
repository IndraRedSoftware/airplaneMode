# Copyright (c) 2024, indrajeet and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import random
import string
from frappe.utils import nowdate, formatdate

class RentPayment(Document):
    def before_save(self):
        if not self.receipt_number:
            self.receipt_number = self.generate_receipt_number()
        
        self.validate_payment()

    def generate_receipt_number(self):
        while True:
            # Generate two random alphabets
            random_alphabets = ''.join(random.choices(string.ascii_uppercase, k=2))

            # Generate three random digits
            random_digits = ''.join(random.choices(string.digits, k=3))

            # Format current date as DDMMMYYYY (e.g., 30AUG2024)
            current_date = formatdate(nowdate(), "ddMMMYYYY").upper()

            # Combine parts to form the receipt number
            receipt_number = f"{random_alphabets}{random_digits}-{current_date}"

            # Check if the receipt number already exists
            if not frappe.db.exists("Rent Payment", {"receipt_number": receipt_number}):
                return receipt_number

    def validate_payment(self):
        if self.payment_date > nowdate():
            frappe.throw(frappe._("Payment date cannot be in the future."))

        # Fetch the lease contract document to check its status
        lease_contract_doc = frappe.get_doc("Lease Contract", self.lease_contract)
        if lease_contract_doc.status != "Active":
            frappe.throw(frappe._("Cannot record payment for an inactive lease contract."))
