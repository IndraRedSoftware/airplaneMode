// Copyright (c) 2024, indrajeet and contributors
// For license information, please see license.txt

frappe.ui.form.on('Crew Member', {
    crew: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        if (row.crew) {
            // Fetch the Role from the Crew Member Doctype
            frappe.db.get_value('Crew Member', row.crew, 'role', (r) => {
                if (r) {
                    // Set the Role field to the fetched value
                    frappe.model.set_value(cdt, cdn, 'role', r.role);
                }
            });
        }
    }
});

