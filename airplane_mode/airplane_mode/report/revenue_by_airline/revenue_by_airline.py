import frappe

def execute(filters=None):
    # Query to get revenue by airline
    query = """
    SELECT
        airline.name AS `Airline`,
        IFNULL(SUM(at.total_amount), 0) AS `Revenue`
    FROM
        `tabAirlines` AS airline
    LEFT JOIN
        `tabAirplanes` AS ap ON airline.name = ap.airline
    LEFT JOIN
        `tabAirplane Flight` AS af ON ap.name = af.airplane
    LEFT JOIN
        `tabAirplane Ticket` AS at ON af.name = at.flight
    GROUP BY
        airline.name
    ORDER BY
        `Revenue` DESC;
    """

    # Execute the query
    data = frappe.db.sql(query, as_dict=True)

    # Prepare the columns for the report
    columns = [
        {"label": "Airline", "fieldname": "Airline", "fieldtype": "Link", "options": "Airlines"},
        {"label": "Revenue", "fieldname": "Revenue", "fieldtype": "Currency"}
    ]
    
	# Calculate total revenue for the summary section
    total_revenue = sum(row['Revenue'] for row in data)
    
    # Prepare data for the donut chart
    chart_data = {
        'data': {
            'labels': [row['Airline'] for row in data],
            'datasets': [{
                'name': 'Revenue',
                'values': [row['Revenue'] for row in data]
            }]
        },
        'type': 'donut',
        'options': {
            'centerText': {
                'value': f"Total Revenue: {total_revenue}",
                'color': '#FF5733',  # Set the text color
                'fontSize': 24,  # Larger font size for visibility
                'fontWeight': 'bold'  # Make the text bold
            }
        }
    }
    
    summary = [
        {
            "label": "Total Revenue",
            "value": total_revenue,
            "indicator": "Green",
            "currency": "USD"
        }
    ]


    # Return data and columns
    return columns, data, None, chart_data, summary

