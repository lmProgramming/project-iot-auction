function handleFormSubmit(event: Event, cardId: number): void {
    event.preventDefault();
    const form = event.target as HTMLFormElement;
    const formData = new FormData(form);
    const url = form.action;

    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken') as string
        }
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.success) {
            alert(`Balance updated successfully. New balance: ${data.new_balance}`);
            const balanceCell = form.closest('tr')?.querySelector('td:nth-child(2)');
            if (balanceCell) {
                balanceCell.textContent = data.new_balance.toString();
            }
        } else {
            alert(`Error: ${data.error}`);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('An error occurred while updating the balance.');
    });
}