class WeatherDashboard {
    constructor() {
        this.apiKey = 'demo'; // In a real app, use a proper API key
        this.baseUrl = 'https://api.openweathermap.org/data/2.5';
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadDefaultCity();
    }

    bindEvents() {
        const searchBtn = document.getElementById('searchBtn');
        const cityInput = document.getElementById('cityInput');

        searchBtn.addEventListener('click', () => this.searchWeather());
        cityInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.searchWeather();
            }
        });
    }

    async loadDefaultCity() {
        await this.getWeatherData('London');
    }

    async searchWeather() {
        const cityInput = document.getElementById('cityInput');
        const city = cityInput.value.trim();
        
        if (!city) {
            this.showError('Please enter a city name');
            return;
        }

        await this.getWeatherData(city);
    }

    async getWeatherData(city) {
        this.showLoading();
        
        try {
            // Since we can't use a real API key in this demo, we'll simulate the data
            const weatherData = this.getMockWeatherData(city);
            const forecastData = this.getMockForecastData(city);
            
            this.displayWeatherData(weatherData, forecastData);
        } catch (error) {
            this.showError('Unable to fetch weather data. Please try again.');
        }
    }

    getMockWeatherData(city) {
        // Mock data for demonstration
        return {
            name: city,
            main: {
                temp: Math.floor(Math.random() * 30) + 5,
                feels_like: Math.floor(Math.random() * 30) + 5,
                humidity: Math.floor(Math.random() * 40) + 40,
                pressure: Math.floor(Math.random() * 100) + 1000
            },
            weather: [{
                main: 'Clear',
                description: 'clear sky',
                icon: '01d'
            }],
            wind: {
                speed: Math.floor(Math.random() * 20) + 5
            }
        };
    }

    getMockForecastData(city) {
        const forecasts = [];
        const weatherTypes = [
            { main: 'Clear', icon: '01d' },
            { main: 'Clouds', icon: '02d' },
            { main: 'Rain', icon: '10d' },
            { main: 'Snow', icon: '13d' }
        ];

        for (let i = 1; i <= 5; i++) {
            const date = new Date();
            date.setDate(date.getDate() + i);
            
            const weather = weatherTypes[Math.floor(Math.random() * weatherTypes.length)];
            
            forecasts.push({
                dt: date.getTime() / 1000,
                main: {
                    temp_max: Math.floor(Math.random() * 25) + 10,
                    temp_min: Math.floor(Math.random() * 15) + 5
                },
                weather: [weather]
            });
        }

        return { list: forecasts };
    }

    displayWeatherData(currentWeather, forecast) {
        // Update current weather
        document.getElementById('cityName').textContent = currentWeather.name;
        document.getElementById('currentDate').textContent = new Date().toLocaleDateString('en-US', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        document.getElementById('currentTemp').textContent = `${Math.round(currentWeather.main.temp)}°C`;
        document.getElementById('weatherDescription').textContent = currentWeather.weather[0].description;
        document.getElementById('feelsLike').textContent = `${Math.round(currentWeather.main.feels_like)}°C`;
        document.getElementById('humidity').textContent = `${currentWeather.main.humidity}%`;
        document.getElementById('windSpeed').textContent = `${Math.round(currentWeather.wind.speed * 3.6)} km/h`;
        document.getElementById('pressure').textContent = `${currentWeather.main.pressure} hPa`;

        // Update weather icon
        const iconUrl = `https://openweathermap.org/img/wn/${currentWeather.weather[0].icon}@2x.png`;
        document.getElementById('weatherIcon').src = iconUrl;

        // Update forecast
        this.displayForecast(forecast.list);

        this.showWeatherData();
    }

    displayForecast(forecastList) {
        const container = document.getElementById('forecastContainer');
        container.innerHTML = '';

        forecastList.forEach(item => {
            const date = new Date(item.dt * 1000);
            const dayName = date.toLocaleDateString('en-US', { weekday: 'short' });
            const iconUrl = `https://openweathermap.org/img/wn/${item.weather[0].icon}.png`;

            const forecastItem = document.createElement('div');
            forecastItem.className = 'forecast-item';
            forecastItem.innerHTML = `
                <div class="forecast-date">${dayName}</div>
                <img class="forecast-icon" src="${iconUrl}" alt="${item.weather[0].main}">
                <div class="forecast-desc">${item.weather[0].main}</div>
                <div class="forecast-temps">
                    <span class="forecast-high">${Math.round(item.main.temp_max)}°</span>
                    <span class="forecast-low">${Math.round(item.main.temp_min)}°</span>
                </div>
            `;
            container.appendChild(forecastItem);
        });
    }

    showLoading() {
        document.getElementById('loading').classList.remove('hidden');
        document.getElementById('error').classList.add('hidden');
        document.getElementById('weatherData').classList.add('hidden');
    }

    showError(message) {
        document.getElementById('error').querySelector('p').textContent = `❌ ${message}`;
        document.getElementById('error').classList.remove('hidden');
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('weatherData').classList.add('hidden');
    }

    showWeatherData() {
        document.getElementById('weatherData').classList.remove('hidden');
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('error').classList.add('hidden');
    }
}

// Initialize the weather dashboard when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new WeatherDashboard();
});