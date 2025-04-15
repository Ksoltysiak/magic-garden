const baseURL = 'http://127.0.0.1:5000';

// Remove the duplicate event listener and keep only this one
document.getElementById('plant-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('name').value;
    const image = document.getElementById('image').value;
    const description = document.getElementById('description').value;
    
    const res = await fetch(`${baseURL}/plants`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, image, description })
    });
    
    const data = await res.json();
    alert(data.message || data.error);
    loadPlants();
});

async function loadPlants() {
    const res = await fetch(`${baseURL}/plants`, {
        method: 'GET',
        credentials: 'include'
    });
    
    const plantList = document.getElementById('plant-list');
    plantList.innerHTML = '';
    
    if (res.status === 200) {
        const plants = await res.json();
        plants.forEach(p => {
            const el = document.createElement('div');
            el.innerHTML = `<h3>${p.name}</h3>
                            <img src="${p.image}" alt="${p.name}" width="200">
                            <p>${p.description}</p><hr>`;
            plantList.appendChild(el);
        });
    } else {
        const error = await res.json();
        plantList.innerHTML = `<p style="color:red">${error.error}</p>`;
    }
}

async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    const res = await fetch(`${baseURL}/login`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    
    const data = await res.json();
    alert(data.message || data.error);
    loadPlants();
}

async function logout() {
    const res = await fetch(`${baseURL}/logout`, {
        method: 'POST',
        credentials: 'include'
    });
    const data = await res.json();
    alert(data.message);
    loadPlants();
}

loadPlants(); // automatycznie po wejściu na stronę