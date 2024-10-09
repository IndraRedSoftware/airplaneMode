import frappe

def get_context(context):
    # Fetch available countries for the filter
    context.countries = frappe.get_all(
        "Airport", 
        fields=["country"], 
        distinct=True, 
        order_by="country"
    )

    # Get the filters from the request (if any)
    selected_country = frappe.form_dict.get("country")
    selected_city = frappe.form_dict.get("city")

    # Base filters dictionary
    filters = {}

    # Apply country filter if selected
    if selected_country:
        filters["country"] = selected_country

        # Fetch cities for the selected country to populate the city filter
        context.cities = frappe.get_all(
            "Airport", 
            filters={"country": selected_country}, 
            fields=["city"], 
            distinct=True, 
            order_by="city"
        )

    # Apply city filter if selected
    if selected_city:
        filters["city"] = selected_city

    # Fetch airports based on the applied filters
    context.airports = frappe.get_all(
        "Airport",
        filters=filters,
        fields=["name", "code", "city", "country"]
    )

    # Pass the selected filters back to the context for display in the template
    context.selected_country = selected_country
    context.selected_city = selected_city
