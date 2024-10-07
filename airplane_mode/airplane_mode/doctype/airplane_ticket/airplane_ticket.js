frappe.ui.form.on('Airplane Ticket', {
    refresh: function(frm) {
        // Add custom button to open seat assignment dialog
        frm.add_custom_button(__('Assign Seat'), function() {
            // Open a dialog to manually input seat number
            let d = new frappe.ui.Dialog({
                title: 'Assign Seat Number',
                fields: [
                    {
                        label: 'Seat Number',
                        fieldname: 'seat_number',
                        fieldtype: 'Data',
                        reqd: 1, // Mandatory input
                        description: 'Please enter a seat number (e.g., 12A, 15B, etc.)'
                    }
                ],
                primary_action_label: 'Set Seat',
                primary_action(values) {
                    if (values.seat_number) {
                        // Set the seat number in the form field
                        frm.set_value('seat', values.seat_number);
                        frm.save();  // Save the form to apply changes
                        d.hide();  // Hide the dialog
                        frappe.msgprint(__('Seat number set to ' + values.seat_number));
                    }
                }
            });
            d.show();
        });
    }
});
