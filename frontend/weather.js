document.addEventListener('DOMContentLoaded', async () => {
    loadCurrentWeather();

    const skyCondition = document.getElementById('sky-condition');
    const precipitation = document.getElementById('precipitation');

    skyCondition.addEventListener('change', validateWeatherForm);
    precipitation.addEventListener('change', validateWeatherForm);

    document.getElementById('weather-form').addEventListener('submit', async (e) => {
        e.preventDefault();

        // Walidacja biznesowa (frontend)
        if (precipitation.checked && skyCondition.value === 'clear') {
            document.getElementById('precip-validation').textContent =
                'Opad atmosferyczny nie może wystąpić przy bezchmurnym niebie!';
            return;
        }

        const weatherData = {
            sky_condition: skyCondition.value,
            temperature: parseInt(document.getElementById('temperature').value),
            humidity: parseInt(document.getElementById('humidity').value),
            precipitation: precipitation.checked
        };

        try {
            const res = await fetch('http://localhost:5000/weather', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(weatherData)
            });

            if (res.ok) {
                alert('Pogoda została zaktualizowana!');
                await loadCurrentWeather();
            } else {
                const errorData = await res.json();
                alert(`Błąd: ${errorData.error || 'Nie udało się zaktualizować pogody'}`);
            }
        } catch (error) {
            console.error('Błąd:', error);
            alert('Wystąpił problem z połączeniem z serwerem.');
        }
    });
});

function validateWeatherForm() {
    const skyCondition = document.getElementById('sky-condition').value;
    const precipitation = document.getElementById('precipitation').checked;
    const validationMessage = document.getElementById('precip-validation');

    if (precipitation && skyCondition === 'clear') {
        validationMessage.textContent = 'Opad atmosferyczny nie może wystąpić przy bezchmurnym niebie!';
    } else {
        validationMessage.textContent = '';
    }
}

async function loadCurrentWeather() {
    try {
        const res = await fetch('http://localhost:5000/weather');
        const weather = await res.json();

        const weatherIcons = {
            'clear': '☀️',
            'partly_cloudy': '⛅',
            'cloudy': '☁️',
            'overcast': '🌥️'
        };

        document.getElementById('weather-display').innerHTML = `
            <div class="weather-display">
                <div class="weather-stat">
                    <div class="weather-icon">${weatherIcons[weather.sky_condition] || '🌡️'}</div>
                    <span>${formatSkyCondition(weather.sky_condition)}</span>
                </div>
                <div class="weather-stat">
                    <div class="weather-icon">🌡️</div>
                    <span>${weather.temperature}°C</span>
                </div>
                <div class="weather-stat">
                    <div class="weather-icon">💧</div>
                    <span>${weather.humidity}%</span>
                </div>
                <div class="weather-stat">
                    <div class="weather-icon">${weather.precipitation ? '🌧️' : '✓'}</div>
                    <span>${weather.precipitation ? 'Opad' : 'Brak opadów'}</span>
                </div>
            </div>
        `;
    } catch (error) {
        console.error('Błąd:', error);
        document.getElementById('weather-display').innerHTML =
            '<p>Nie udało się pobrać pogody. Sprawdź połączenie.</p>';
    }
}

function formatSkyCondition(condition) {
    const map = {
        'clear': 'Bezchmurne niebo',
        'partly_cloudy': 'Częściowe zachmurzenie',
        'cloudy': 'Pochmurno',
        'overcast': 'Całkowite zachmurzenie'
    };
    return map[condition] || condition;
}
