async function fetchStatus() {
    try {
        const response = await fetch('http://127.0.0.1:5001/tube_status');
        const data = await response.json();
        
        const container = document.getElementById('status-container');
        container.innerHTML = ''; 

        data.forEach(line => {
            const card = document.createElement('div');
            card.classList.add('status-card');
            
            // Format class name for CSS (e.g., "Good Service" -> "good-service")
            const statusClass = line.status.toLowerCase().replace(" ", "-");
            
            card.innerHTML = `
                <span class="line-name">${line.name}</span>
                <span class="status-text ${statusClass}">
                    ${line.status}
                </span>
            `;
            container.appendChild(card);
        });
    } catch (error) {
        console.error("Error:", error);
    }
}

fetchStatus();
// Auto-refresh every minute so it's always live
setInterval(fetchStatus, 60000);