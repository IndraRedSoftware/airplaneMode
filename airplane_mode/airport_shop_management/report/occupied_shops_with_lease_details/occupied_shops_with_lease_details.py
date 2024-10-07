import frappe
from frappe import _

def get_filters():
    # Define the filters that will appear in the report
    return [
        {"fieldname": "airport", "label": _("Airport"), "fieldtype": "Link", "options": "Airport", "default": None},
        {"fieldname": "status", "label": _("Shop Status"), "fieldtype": "Select", "options": "\nAvailable\nOccupied", "default": "Occupied"},
        {"fieldname": "lease_status", "label": _("Lease Status"), "fieldtype": "Select", "options": "\nActive\nExpired", "default": "Active"}
    ]

def execute(filters=None):
    columns, data = [], []

    # Define the columns for the report
    columns = [
        {"label": _("Shop Number"), "fieldname": "shop_number", "fieldtype": "Data", "width": 150},
        {"label": _("Shop Name"), "fieldname": "shop_name", "fieldtype": "Data", "width": 150},
        {"label": _("Tenant Name"), "fieldname": "tenant_name", "fieldtype": "Data", "width": 150},
        {"label": _("Rent Amount"), "fieldname": "rent_amount", "fieldtype": "Currency", "width": 100},
        {"label": _("Lease Start Date"), "fieldname": "lease_start_date", "fieldtype": "Date", "width": 100},
        {"label": _("Lease End Date"), "fieldname": "lease_end_date", "fieldtype": "Date", "width": 100},
        {"label": _("Airport"), "fieldname": "airport", "fieldtype": "Link", "options": "Airport", "width": 100},
    ]

    # Build query with filters
    query = """
        SELECT
            s.shop_number,
            s.shop_name,
            t.tenant_name,
            lc.rent_amount,
            lc.lease_start_date,
            lc.lease_end_date,
            s.airport
        FROM
            `tabShop` s
        INNER JOIN
            `tabLease Contract` lc ON lc.shop = s.name
        INNER JOIN
            `tabTenant` t ON t.name = lc.tenant
        WHERE
            s.status = %s
    """

    # Parameters for the query based on filters
    query_params = [filters.status or "Occupied"]

    # Add filter for airport if provided
    if filters.get("airport"):
        query += " AND s.airport = %s"
        query_params.append(filters.get("airport"))

    # Add filter for lease status if provided
    if filters.get("lease_status"):
        query += " AND lc.status = %s"
        query_params.append(filters.get("lease_status"))

    # Execute the query and fetch data
    data = frappe.db.sql(query, query_params, as_dict=True)

    return columns, data
