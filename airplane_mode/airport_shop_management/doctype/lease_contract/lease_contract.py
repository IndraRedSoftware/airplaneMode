import frappe
from frappe.model.document import Document

class LeaseContract(Document):
    def before_save(self):
        # Fetch the shop document
        if self.shop:
            shop_name = self.shop
            shop_doc = frappe.get_doc("Shop", shop_name)

            # Check if the shop is occupied
            if shop_doc.status == "Occupied":
                # Throw a validation error if the shop is already occupied
                frappe.throw(f"The shop '{shop_name}' is already occupied and cannot have a new lease contract.")

            # Otherwise, proceed to mark the shop as occupied
            shop_doc.status = "Occupied"  # Set the shop status to "Occupied"
            shop_doc.save()  # Save the changes to the shop document
