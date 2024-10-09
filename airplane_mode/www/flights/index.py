import frappe
from frappe.utils import nowdate

def get_context(context):
    # Get user input from the request (query parameters)
    source_airport = frappe.form_dict.get('source_airport')
    destination_airport = frappe.form_dict.get('destination_airport')
    departure_date = frappe.form_dict.get('departure_date')

    # Prepare filters based on the input
    filters = {}

    if source_airport:
        filters['source_airport'] = source_airport
    if destination_airport:
        filters['destination_airport'] = destination_airport
    if departure_date:
        filters['date_of_departure'] = departure_date

    filters['date_of_departure'] = ['>=', nowdate()]

    # Fetch flights based on filters (if any)
    context.flights = frappe.get_all(
        "Airplane Flight",
        filters=filters if filters else None,
        fields="*"
    )

    # Load available airports for the form dropdowns
    context.airports = frappe.get_all(
        "Airport",
        fields=["name", "code"]
    )
