# Copyright (c) 2024, indrajeet and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
import random


class AirplaneTicket(Document):
    def before_insert(self):
        random_integer = random.randint(1, 99)
        random_letter = random.choice('ABCDE')
        self.seat = f"{random_integer}{random_letter}"

    def validate(self):
        # Remove duplicate add-ons and calculate total amount
        self.remove_duplicate_addons()
        self.calculate_total_amount()
        self.check_flight_capacity()

    def check_flight_capacity(self):
        # Fetch the flight document linked to the ticket
        flight = frappe.get_doc("Airplane Flight", self.flight)
        
        # Fetch the airplane linked to the flight
        airplane = frappe.get_doc("Airplanes", flight.airplane)

        # Get the number of tickets already created for this flight
        ticket_count = frappe.db.count("Airplane Ticket", filters={"flight": self.flight})

        # Check if the number of tickets exceeds the airplane capacity
        if ticket_count >= airplane.capacity:
            frappe.throw(_("Cannot create ticket. The airplane for this flight is fully booked. Capacity: {0}".format(airplane.capacity)))


    def remove_duplicate_addons(self):
        # Use a set to track unique add-ons
        seen_addons = set()
        unique_addons = []

        # Loop through add-ons in the child table
        for addon in self.add_ons:
            if addon.item not in seen_addons:
                # Add the item to the set if not seen
                seen_addons.add(addon.item)
                unique_addons.append(addon)
            else:
                # Duplicate found, ignore it
                frappe.msgprint(f"Duplicate add-on {addon.item} removed.", alert=True)

        # Replace the original list of add-ons with the unique add-ons
        self.add_ons = unique_addons

    def calculate_total_amount(self):
        # Initialize total amount with flight price
        total_amount = self.flight_price or 0

        # Add the amounts from all the add-ons
        for addon in self.add_ons:
            total_amount += addon.amount

        # Set the total amount in the doc
        self.total_amount = total_amount


# Validation function for preventing submission if status is not 'Boarded'
def validate_status_before_submission(doc, method):
    # Check if the status is 'Boarded'
    if doc.status != "Boarded":
        # Throw an error to prevent submission
        frappe.throw(_("The Airplane Ticket cannot be submitted unless the status is 'Boarded'."))

