import frappe

def get_context(context):
    # Fetch distinct airports
    context.airports = frappe.get_all(
        "Airport",
        fields=[ "name", "code", "city", "country"]
    )

