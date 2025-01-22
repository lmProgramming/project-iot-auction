"use strict";
function handleFormSubmit(event, cardId) {
    event.preventDefault();
    var form = event.target;
    var formData = new FormData(form);
    var url = form.action;
    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        }
    })
        .then(function (response) { return response.json(); })
        .then(function (data) {
        var _a;
        if (data.success) {
            alert("Balance updated successfully. New balance: ".concat(data.new_balance));
            var balanceCell = (_a = form.closest('tr')) === null || _a === void 0 ? void 0 : _a.querySelector('td:nth-child(2)');
            if (balanceCell) {
                balanceCell.textContent = data.new_balance.toString();
            }
        }
        else {
            alert("Error: ".concat(data.error));
        }
    })
        .catch(function (error) {
        console.error('Error:', error);
        alert('An error occurred while updating the balance.');
    });
}
