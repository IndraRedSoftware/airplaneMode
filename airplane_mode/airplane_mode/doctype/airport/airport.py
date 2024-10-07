from frappe.model.document import Document
import frappe

class Airport(Document):
    def __init__(self, *args, **kwargs):
        super(Airport, self).__init__(*args, **kwargs)
        self.is_updating = False  # Initialize the flag

    def on_update(self):
        # Update shop counts only if not already updating
        if not self.is_updating:
            self.update_shop_counts()

    def update_shop_counts(self):
        # Set the flag to avoid recursion
        self.is_updating = True
        
        # Count total shops
        total_shops = frappe.db.count('Shop', {'airport': self.name})
        self.total_shops = total_shops

        # Count available shops
        available_shops = frappe.db.count('Shop', {'airport': self.name, 'status': 'Available'})
        self.available_shops = available_shops

        # Save the updated counts
        self.save()

        # Unset the flag
        self.is_updating = False
