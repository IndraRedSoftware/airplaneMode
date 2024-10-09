frappe.ui.form.on('Tenant', {
    refresh: function(frm) {
        if (frm.doc.name) {
            // Fetch all lease contracts for the tenant
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'Lease Contract',
                    filters: {
                        tenant: frm.doc.name
                    },
                    fields: ['shop']
                },
                callback: function(response) {
                    if (response.message) {
                        let shop_list = response.message.map(shop => shop.shop);
                        let shop_links = shop_list.map(shop => `<a href="/app/shop/${shop}" target="_blank">${shop}</a>`).join(', ');

                        // Add the list of shops to the tenant form
                        frm.dashboard.add_section(`<strong>Shops Acquired:</strong> ${shop_links}`);
                    }
                }
            });
        }
    }
});
