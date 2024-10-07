import frappe

def get_context(context):
    # The flight ID will be extracted from the URL as part of the route
    flight_id = frappe.form_dict.get('name')  # Extract flight ID from the URL path
    if flight_id:
        context.flight = frappe.get_doc("Airplane Flight", flight_id)
    else:
        frappe.throw("Flight not found", frappe.DoesNotExistError)
