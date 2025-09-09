// Fetch processed data and render
fetch('data/processed/dashboard.json')
    .then(response => response.json())
    .then(data => {
        // Placeholder for chart rendering (e.g., using Chart.js)
        console.log('Data loaded:', data);
    });