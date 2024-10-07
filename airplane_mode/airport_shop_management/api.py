import frappe
from frappe.utils import nowdate, add_days, get_last_day, today, date_diff, formatdate

def send_rent_reminders():
    settings = frappe.get_single('Shop Settings')
    if not settings.enable_rent_reminders:
        return

    # Get all active lease contracts that haven't expired
    active_contracts = frappe.get_all("Lease Contract", 
        filters={
            "status": "Active", 
            "lease_end_date": [">=", nowdate()]  # Ensure the contract has not expired
        }, 
        fields=["tenant", "shop", "rent_amount", "lease_start_date", "lease_end_date"])

    for contract in active_contracts:
        tenant = frappe.get_doc("Tenant", contract.tenant)

        # Send rent reminder two days before the end of the current month
        last_day_of_month = get_last_day(today())
        reminder_date = add_days(last_day_of_month, -2)

        if nowdate() == reminder_date:
            # Send rent reminder email
            frappe.sendmail(
                recipients=tenant.email,
                subject="Rent Payment Reminder",
                message=f"Dear {tenant.tenant_name},<br><br>Your rent payment of {contract.rent_amount} is due by the end of this month. Please ensure that you make the payment at your earliest convenience.<br><br>Thank you!",
                delayed=False
            )

        # Send reminder before the lease contract expiration (e.g., 7 days before)
        expiration_reminder_date = add_days(contract.lease_end_date, -7)

        if nowdate() == expiration_reminder_date:
            # Send expiration reminder email
            frappe.sendmail(
                recipients=tenant.email,
                subject="Lease Contract Expiration Reminder",
                message=f"Dear {tenant.tenant_name},<br><br>Your lease contract for the shop {contract.shop} is expiring on {formatdate(contract.lease_end_date)}. Please contact us if you wish to renew or if you have any questions.<br><br>Thank you!",
                delayed=False
            )
