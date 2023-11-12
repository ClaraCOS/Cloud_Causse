from flask import Flask, jsonify, request, render_template, render_template_string
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuration de la base de données PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:user@db:5432/mybd'
db = SQLAlchemy(app)

# Modèle de données pour les connexions
class Connexion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Créez la table "Connexion" si elle n'existe pas
with app.app_context():
    db.create_all()

# Modèle HTML directement dans la chaîne de caractères
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Historique des Connexions</title>
</head>
<body>
    <h1>Historique des Connexions</h1>
    {% if connexions %}
        <ul>
        {% for connexion in connexions %}
            <li>{{ connexion.name }} - {{ connexion.timestamp }}</li>
        {% endfor %}
        </ul>
    {% else %}
        <p>Aucune connexion enregistrée pour le moment.</p>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def get_connexions():
    # Récupérez toutes les connexions depuis la base de données
    connexions = Connexion.query.all()

    return render_template_string(html_template, connexions=connexions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
