from flask import Flask, render_template, jsonify

app = Flask(__name__)

TOUR_PACKAGE = [
  {
    'id': 1,
    'title': 'Vietnam',
    'duration': '7 days',
    'price': 'Starting at $600'
  },
  {
    'id': 2,
    'title': 'Laos',
    'duration': '4 days',
    'price': 'Starting at $350'
  },
  {
    'id': 3,
    'title': 'Cambodia',
    'duration': '4 days',
    'price': 'Starting at $360'
  },
  {
    'id': 4,
    'title': 'Thailand',
    'duration': '5 days',
    'price': 'Starting at $600'
  }
]

@app.route("/")
def hello_world():
  return render_template('home.html', deals=TOUR_PACKAGE)

@app.route("/api/tours")
def list_tours():
  return jsonify(TOUR_PACKAGE)

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)