import frappe

def get_context(context):
    # Check if the user is not logged in (Guest)
    context.is_guest = frappe.session.user == "Guest"

    # Fetch the flight from the URL parameter
    flight_name = frappe.form_dict.get('flight')
    frappe.logger().info(f"Flight parameter from URL: {flight_name}")

    # Fetch flight details if available
    flight = frappe.get_doc('Airplane Flight', flight_name) if flight_name else None
    context.flight = flight

    # Log the fetched flight document
    frappe.logger().info(f"Fetched flight document: {flight}")

    # Add CSRF token to the context for form submissions
    context.csrf_token = frappe.sessions.get_csrf_token()



@frappe.whitelist()
def book_flight_ticket(flight, passenger):
    try:
        # Log the user attempting to book a ticket
        print("Attempting to book a ticket by user: " + frappe.session.user)

        # Check if the user is logged in
        if frappe.session.user == "Guest":
            current_url = frappe.local.request.url
            print(current_url)
            # Redirect to login page for guest users
            frappe.local.response["type"] = "redirect"
            frappe.local.response["location"] = f"/login?redirect_to={current_url}"
            return

        # Fetch flight details
        flight_data = frappe.get_doc("Airplane Flight", flight)

        # Create a new Airplane Ticket
        ticket = frappe.get_doc({
            "doctype": "Airplane Ticket",
            "flight": flight,
            "passenger": passenger,
            "source_airport_code": flight_data.source_airport_code,
            "destination_airport_code": flight_data.destination_airport_code,
            "departure_date": flight_data.date_of_departure,
            "departure_time": flight_data.time_of_departure,
            "flight_price": flight_data.flight_price,
            "duration_of_flight": flight_data.duration,
            "status": "Booked",
        })

        # Insert the ticket into the database
        ticket.insert(ignore_permissions=True)
        frappe.db.commit()

        # Return a success message as JSON response
        frappe.local.response["type"] = "json"
        return {"message": f"Flight ticket for {passenger} successfully booked!"}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Booking Error")

        # Ensure a JSON response is returned for errors as well
        frappe.local.response["type"] = "json"
        return {"error": f"An error occurred: {str(e)}"}, 500