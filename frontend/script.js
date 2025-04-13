document.getElementById('plant-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('name').value;
    const image = document.getElementById('image').value;
    const description = document.getElementById('description').value;

    const res = await fetch('http://localhost:5000/plants', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, image, description })
    });

    if (res.ok) {
        alert('Roślina dodana!');
        await loadPlants();
    } else {
        alert('Błąd przy dodawaniu rośliny.');
    }
});

async function loadPlants() {
    const res = await fetch('http://localhost:5000/plants');
    const plants = await res.json();
    const container = document.getElementById('plant-list');
    container.innerHTML = '';
    plants.forEach(p => {
        container.innerHTML += `
      <div style="margin-bottom: 20px;">
        <strong>${p.name}</strong><br>
        <img src="${p.image}" width="100" alt=""><br>
        <p>${p.description}</p>
      </div>
    `;
    });
}
