from flask import Blueprint, request, render_template, jsonify, session, make_response, request
from .weather import get_weather, get_city_suggestions
from .models import db, WeatherHistory
import requests

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    weather_info = None
    last_city = request.cookies.get('city')

    if request.method == 'POST':
        city = request.form['city']
        weather_info = get_weather(city)
        session['last_city'] = city
        history = WeatherHistory(city=city)
        db.session.add(history)
        db.session.commit()
        response = make_response(render_template('index.html', weather_info=weather_info, last_city=city))
        response.set_cookie('city', city)
        return response

    return render_template('index.html', weather_info=weather_info, last_city=last_city)

@bp.route('/autocomplete')
def autocomplete():
    query = request.args.get('query')
    if not query:
        return jsonify([])

    try:
        response = requests.get(f'https://secure.geonames.org/searchJSON?name_startsWith={query}&maxRows=5&username=impro')
        response.raise_for_status()  # Поднимает исключение для HTTP ошибок
        data = response.json()
        cities = [{'name': city['name']} for city in data['geonames']]
        return jsonify(cities)
    except requests.RequestException as e:
        # Логирование ошибки
        bp.logger.error(f'Error fetching city suggestions: {e}')
        return jsonify([]), 500

@bp.route('/history', methods=['GET'])
def history():
    last_city = session.get('last_city', None)
    return render_template('history.html', last_city=last_city)

@bp.route('/api/history', methods=['GET'])
def api_history():
    history = WeatherHistory.query.all()
    city_counts = {}
    for record in history:
        city_counts[record.city] = city_counts.get(record.city, 0) + 1
    return jsonify(city_counts)
