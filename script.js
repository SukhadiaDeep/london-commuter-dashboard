async function fetchStatus() {
    try {
        const response = await fetch('http://127.0.0.1:5001/tube_status');
        const data = await response.json();
        const container = document.getElementById('status-container');
        container.innerHTML = ''; 

        data.forEach(line => {
            const card = document.createElement('div');
            card.classList.add('status-card');
            const statusClass = line.status.toLowerCase().replace(/\s+/g, '-');
            
            card.innerHTML = `
                <span class="line-name">${line.name}</span>
                <span class="status-text ${statusClass}">${line.status}</span>
            `;
            container.appendChild(card);
        });
    } catch (e) { console.error("Status Error:", e); }
}

async function fetchArrivals() {
    const stationId = '940GZZLUOXC'; // Oxford Circus
    try {
        const response = await fetch(`http://127.0.0.1:5001/arrivals/${stationId}`);
        const data = await response.json();
        const list = document.getElementById('arrivals-list');
        list.innerHTML = '';

        data.forEach(train => {
            const row = document.createElement('div');
            row.className = 'arrival-row';
            row.innerHTML = `
                <strong>${train.line}</strong> to ${train.destination} 
                <span class="time">${train.minutes} mins</span>
            `;
            list.appendChild(row);
        });
    } catch (e) { console.error("Arrivals Error:", e); }
}

// --- INITIALIZE BOTH ---
fetchStatus();
fetchArrivals();

// --- REFRESH BOTH ---
setInterval(fetchStatus, 60000); // Lines every 1 min
setInterval(fetchArrivals, 30000); // Arrivals every 30 secs