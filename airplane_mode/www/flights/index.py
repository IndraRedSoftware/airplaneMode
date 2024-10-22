import frappe
from frappe.utils import nowdate

def get_context(context):
    # Get user input from the request (query parameters)
    source_city = frappe.form_dict.get('source_city')
    destination_city = frappe.form_dict.get('destination_city')
    departure_date = frappe.form_dict.get('departure_date')

    print(f"Source City: {source_city}, Destination City: {destination_city}, Departure Date: {departure_date}")

    # Prepare filters based on the input
    filters = {}

    # Fetch airport codes based on the cities selected
    if source_city:
        source_airports = frappe.get_all(
            "Airport",
            filters={"city": source_city},
            fields=["code"]
        )
        if source_airports:
            source_codes = [airport['code'] for airport in source_airports]
            # Always use 'IN' for multiple codes
            filters['source_airport_code'] = ['IN', source_codes] if len(source_codes) > 1 else source_codes[0]

    if destination_city:
        destination_airports = frappe.get_all(
            "Airport",
            filters={"city": destination_city},
            fields=["code"]
        )
        if destination_airports:
            destination_codes = [airport['code'] for airport in destination_airports]
            # Always use 'IN' for multiple codes
            filters['destination_airport_code'] = ['IN', destination_codes] if len(destination_codes) > 1 else destination_codes[0]

    # Always filter by current or future flights
    filters['date_of_departure'] = ['>=', nowdate()]

    if departure_date:
        filters['date_of_departure'] = departure_date  # Override with specific departure date if provided


    # Fetch flights based on filters
    context.flights = frappe.get_all(
        "Airplane Flight",
        filters=filters,
        fields="*"
    )


    # Fetch all distinct cities from the Airport Doctype for dropdowns
    context.cities = frappe.db.sql_list("SELECT DISTINCT city FROM `tabAirport` WHERE city IS NOT NULL")

    # Load available airports for the form dropdowns
    context.airports = frappe.get_all(
        "Airport",
        fields=["name", "code", "city"]
    )
