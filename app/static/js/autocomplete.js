document.addEventListener('DOMContentLoaded', () => {
    const cityInput = document.getElementById('city-input');
    const suggestions = document.createElement('ul');
    suggestions.classList.add('suggestions');
    cityInput.parentNode.insertBefore(suggestions, cityInput.nextSibling);

    cityInput.addEventListener('input', async () => {
        const query = cityInput.value.trim();
        if (query.length < 3) {
            clearSuggestions();
            return;
        }

        try {
            const response = await fetch(`/autocomplete?query=${query}`);
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }
            const data = await response.json();
            updateSuggestions(data);
        } catch (error) {
            console.error('Error fetching city suggestions:', error);
        }
    });

    document.addEventListener('click', (event) => {
        if (!suggestions.contains(event.target) && event.target !== cityInput) {
            clearSuggestions();
        }
    });

    function clearSuggestions() {
        suggestions.innerHTML = '';
    }

    function updateSuggestions(cities) {
        clearSuggestions();
        cities.forEach(city => {
            const li = document.createElement('li');
            li.textContent = city.name;
            li.addEventListener('click', () => {
                cityInput.value = city.name;
                clearSuggestions();
            });
            suggestions.appendChild(li);
        });
    }

    const style = document.createElement('style');
    style.innerHTML = `
        .suggestions {
            position: absolute;
            border: 1px solid #ccc;
            max-height: 150px;
            overflow-y: auto;
            z-index: 1000;
            background-color: white;
            margin-top: 0;
        }
        .suggestions li {
            padding: 5px;
            cursor: pointer;
        }
        .suggestions li:hover {
            background-color: #eee;
        }
    `;
    document.head.appendChild(style);
});
