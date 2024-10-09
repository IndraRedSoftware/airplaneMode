import frappe

def get_context(context):
    # Initialize filters
    filters = {}

    # Check for airport filter
    if frappe.form_dict.get('airport'):
        filters['airport'] = frappe.form_dict.get('airport')
        print(f"Airport filter applied: {filters['airport']}")

    # Fetch all shops along with tenant info for occupied shops
    sql_query = """
        SELECT 
            s.shop_name, 
            s.status, 
            s.shop_number,
            s.shop_image, 
            s.area,
            s.airport,
            t.tenant_name, 
            t.email, 
            t.phone_number 
        FROM 
            `tabShop` s 
        LEFT JOIN 
            `tabLease Contract` lc ON s.name = lc.shop
        LEFT JOIN 
            `tabTenant` t ON lc.tenant = t.name
        ORDER BY 
            s.creation DESC  -- Sort by creation date, newest first
    """

    # Add airport filter if provided
    params = []
    if filters.get('airport'):
        sql_query += " WHERE s.airport = %s"
        params.append(filters['airport'])

    # Execute the query to fetch all shops with tenant info where applicable
    context.shops = frappe.db.sql(sql_query, tuple(params), as_dict=True)

    print("Fetched Shops with Tenant Information:")
    if context.shops:
        for shop in context.shops:
            print(f"Shop Name: {shop.shop_name}, Tenant Name: {shop.tenant_name}, Email: {shop.email}, Phone: {shop.phone_number}")
    else:
        print("No shops found.")

    # Fetch distinct airports for filtering if needed
    context.airports = frappe.get_all(
        "Shop",
        fields=["airport"],
        distinct=True
    )
