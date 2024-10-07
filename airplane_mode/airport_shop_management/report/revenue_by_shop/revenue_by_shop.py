import frappe

def execute(filters=None):
    # Query to get revenue by shop
    query = """
    SELECT
        s.shop_number AS `Shop`,
        s.airport AS `Airport`,
        IFNULL(SUM(rp.rent_amount), 0) AS `Revenue`
    FROM
        `tabShop` AS s
    LEFT JOIN
        `tabLease Contract` AS lc ON s.name = lc.shop
    LEFT JOIN
        `tabRent Payment` AS rp ON lc.name = rp.lease_contract
    WHERE
        s.status = 'Occupied' 
        AND (lc.status = 'Active' OR lc.status IS NULL)
    GROUP BY
        s.shop_name
    ORDER BY
        `Revenue` DESC;
    """

    # Execute the query
    data = frappe.db.sql(query, as_dict=True)

    # Prepare the columns for the report
    columns = [
        {"label": "Shop", "fieldname": "Shop", "fieldtype": "Link", "options": "Shop"},
        {"label": "Airport", "fieldname": "Airport", "fieldtype": "Link", "options": "Airport"},
        {"label": "Revenue", "fieldname": "Revenue", "fieldtype": "Currency"}
    ]
    
    # Calculate total revenue for the summary section
    total_revenue = sum(row['Revenue'] for row in data)
    
    # Prepare data for the donut chart
    chart_data = {
        'data': {
            'labels': [row['Shop'] for row in data],
            'datasets': [{
                'name': 'Revenue',
                'values': [row['Revenue'] for row in data]
            }]
        },
        'type': 'donut',
        'options': {
            'centerText': {
                'value': f"Total Revenue: ₹ {total_revenue}",
                'color': '#FF5733',  # Set the text color
                'fontSize': 24,  # Larger font size for visibility
                'fontWeight': 'bold'  # Make the text bold
            }
        }
    }
    
    # Summary for total revenue
    summary = [
        {
            "label": "Total Revenue",
            "value": f"₹ {total_revenue}",
            "indicator": "Green",
            "currency": "INR"
        }
    ]

    # Return data and columns
    return columns, data, None, chart_data, summary
