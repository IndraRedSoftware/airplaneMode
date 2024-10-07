from frappe.model.document import Document
import frappe

class Shop(Document):
    def after_insert(self):
        self.update_airport_shop_counts()

    def on_update(self):
        # Update counts only if status changed
        if self.is_status_changed():
            self.update_airport_shop_counts()

    def is_status_changed(self):
        # Check if the status has changed
        if self.get_doc_before_save():
            old_status = self.get_doc_before_save().status
            return old_status != self.status
        return False

    def update_airport_shop_counts(self):
        airport = self.airport  # Assuming this is the airport link field
        if airport:
            airport_doc = frappe.get_doc('Airport', airport)
            # Update shop counts only if not already updating
            if not airport_doc.is_updating:
                airport_doc.update_shop_counts()
