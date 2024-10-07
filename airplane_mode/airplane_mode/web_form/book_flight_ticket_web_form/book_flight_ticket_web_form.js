frappe.ready(function() {
    // Get flight from the URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const flightId = urlParams.get('flight');
    
    if (flightId) {
        // Set the flight field in the form
        frappe.web_form.set_value('flight', flightId);
        
        // Fetch flight details using Frappe API
        frappe.call({
            method: 'frappe.client.get',
            args: {
                doctype: 'Airplane Flight',
                name: flightId
            },
            callback: function(response) {
                if (response.message) {
                    const flight = response.message;
                    // Set the flight price in the form
                    frappe.web_form.set_value('flight_price', flight.flight_price);
                }
            }
        });
    }
});
