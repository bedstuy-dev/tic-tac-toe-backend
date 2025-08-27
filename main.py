from flask import Flask, jsonify
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
CORS(app)
SCORES_FILE = 'scores.csv'

# Ensure the scores file exists with initial scores
def initialize_scores():
    if not os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['player1', 0])
            writer.writerow(['player2', 0])

# Load scores from CSV into a dictionary
def load_scores():
    scores = {}
    with open(SCORES_FILE, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                scores[row[0]] = int(row[1])
    return scores

# Save scores dictionary to CSV
def save_scores(scores):
    with open(SCORES_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        for player, score in scores.items():
            writer.writerow([player, score])

@app.route('/scores', methods=['GET'])
def get_scores():
    scores = load_scores()
    return jsonify(scores)

@app.route('/score/<player>', methods=['POST'])
def increment_score(player):
    scores = load_scores()
    if player not in scores:
        return jsonify({'error': 'Player not found'}), 404

    scores[player] += 1
    save_scores(scores)
    return jsonify({player: scores[player]})

if __name__ == '__main__':
    initialize_scores()
    app.run(debug=True)
