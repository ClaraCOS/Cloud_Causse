from flask import Flask, request, render_template, render_template_string
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuration de la base de données PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:user@db:5432/mybd'
db = SQLAlchemy(app)

# Modèle de données
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
    <title>Connexion Form</title>
</head>
<body>
    <h1>Entrez votre prénom</h1>
    <form method="post" action="/">
        <label for="first_name">Prénom:</label>
        <input type="text" id="first_name" name="first_name" required>
        <button type="submit">Envoyer</button>
    </form>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        # Obtenir le prénom depuis le formulaire
        first_name = request.form.get('first_name')

        # Obtenir l'heure actuelle
        current_time = datetime.utcnow()

        # Exemple d'ajout d'une nouvelle connexion à la base de données avec le prénom
        new_connexion = Connexion(name=f'{first_name}', timestamp=current_time)
        db.session.add(new_connexion)
        db.session.commit()

        return 'Une nouvelle connexion a été ajoutée avec succès à la base de données avec le prénom et l\'heure de connexion!'

    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
