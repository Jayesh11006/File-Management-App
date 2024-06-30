function handleFormSubmission(formId, endpoint) {
    document.getElementById(formId).addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        fetch(endpoint, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById('results');
            resultsDiv.style.display = 'block';
            resultsDiv.innerHTML = '';
            data.forEach(item => {
                const p = document.createElement('p');
                p.textContent = item;
                resultsDiv.appendChild(p);
            });
        })
        .catch(error => console.error('Error:', error));
    });
}

// event listeners to forms
handleFormSubmission('rename-form', '/rename');
handleFormSubmission('undo-form', '/undo');
