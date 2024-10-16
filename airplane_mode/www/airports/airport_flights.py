import frappe

def get_context(context):
    # Dynamically fetch the airport code from the URL parameters
    airport_code = frappe.form_dict.get('airport_code') or context.get('airport_code')
    print(airport_code)

    if not airport_code:
        frappe.throw("Airport code not provided in the URL.")

    # Fetch the airport details using the dynamic airport code
    airport = frappe.db.get_value("Airport", {"code": airport_code}, ["name", "city", "code"])

    # Check if the airport exists
    if not airport:
        frappe.throw(f"Airport with code {airport_code} not found.")

    # Fetch the flights departing from this airport
    flights = frappe.get_all("Airplane Flight", filters={"source_airport_code": airport_code},fields="*")

    # Pass the airport and flights data to the context
    context.airport = airport
    context.flights = flights
