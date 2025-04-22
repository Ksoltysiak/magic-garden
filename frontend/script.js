const baseURL = 'http://127.0.0.1:5000';
let currentEditId = null; // Śledzi ID rośliny w trakcie edycji

// Obsługa formularza dodawania/edycji rośliny
document.getElementById('plant-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('name').value;
    const image = document.getElementById('image').value;
    const description = document.getElementById('description').value;

    try {
        let response;
        if (currentEditId) {
            // Aktualizacja istniejącej rośliny
            response = await fetch(`${baseURL}/plants/${currentEditId}`, {
                method: 'PUT',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, image, description })
            });
        } else {
            // Dodawanie nowej rośliny
            response = await fetch(`${baseURL}/plants`, {
                method: 'POST',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, image, description })
            });
        }

        const data = await response.json();
        if (!response.ok) throw new Error(data.error || 'Nieznany błąd');

        alert(data.message);
        resetForm();
        await loadPlants();
    } catch (error) {
        alert(error.message);
    }
});

// Pobieranie i wyświetlanie listy roślin
async function loadPlants() {
    try {
        const response = await fetch(`${baseURL}/plants`, {
            method: 'GET',
            credentials: 'include'
        });

        const plantList = document.getElementById('plant-list');
        plantList.innerHTML = '';

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error);
        }

        const plants = await response.json();
        plants.forEach(p => {
            const plantDiv = document.createElement('div');
            plantDiv.className = 'plant-item';
            plantDiv.innerHTML = `
                <h3>${p.name}</h3>
                <img src="${p.image}" alt="${p.name}" width="200">
                <p>${p.description}</p>
                <div class="plant-actions">
                    <button class="edit-btn" onclick="startEditPlant(${p.id}, '${p.name}', '${p.image}', '${p.description.replace(/'/g, "\\'")}')">✏️ Edytuj</button>
                    <button class="delete-btn" onclick="deletePlant(${p.id})">🗑️ Usuń</button>
                </div>
                <hr>
            `;
            plantList.appendChild(plantDiv);
        });
    } catch (error) {
        plantList.innerHTML = `<p class="error-message">❌ ${error.message}</p>`;
    }
}

// Usuwanie rośliny z potwierdzeniem
async function deletePlant(id) {
    if (!confirm('Czy na pewno chcesz usunąć tę roślinę?')) return;

    try {
        const response = await fetch(`${baseURL}/plants/${id}`, {
            method: 'DELETE',
            credentials: 'include'
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error);
        }

        alert('Roślina została usunięta');
        loadPlants();
    } catch (error) {
        alert(error.message);
    }
}

// Przygotowanie formularza do edycji istniejącej rośliny
function startEditPlant(id, name, image, description) {
    currentEditId = id;
    document.getElementById('name').value = name;
    document.getElementById('image').value = image;
    document.getElementById('description').value = description;
    document.getElementById('plant-form').scrollIntoView();
}

// Resetowanie formularza po sukcesie
function resetForm() {
    currentEditId = null;
    document.getElementById('plant-form').reset();
}

// Logowanie użytkownika
async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${baseURL}/login`, {
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.error);

        alert(data.message);
        loadPlants();
    } catch (error) {
        alert(error.message);
    }
}

// Wylogowywanie użytkownika
async function logout() {
    try {
        const response = await fetch(`${baseURL}/logout`, {
            method: 'POST',
            credentials: 'include'
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error);
        }

        alert('Wylogowano pomyślnie');
        loadPlants();
    } catch (error) {
        alert(error.message);
    }
}

// Automatyczne ładowanie roślin przy starcie aplikacji
loadPlants();
