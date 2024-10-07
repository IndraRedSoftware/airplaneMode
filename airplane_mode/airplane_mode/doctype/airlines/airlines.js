frappe.ui.form.on('Airlines', {
    refresh: function(frm) {
        if (frm.doc.website) {
            console.log('Website URL found: ' + frm.doc.website);

            // Remove the section argument to place the button at the top
            frm.add_custom_button(__('Visit Website'), function() {
                window.open(frm.doc.website, '_blank'); // Open website in a new tab
            }).addClass('btn-primary'); // Optional: style the button

            console.log('Button should be added now');
        } else {
            console.log('No Website URL found.');
        }
    }
});
