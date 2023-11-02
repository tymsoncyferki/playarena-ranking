from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.app_context().push()


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rank = db.Column(db.Integer, default=0)
    team = db.Column(db.String(150), nullable=True)
    image = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'Player {self.id}: {self.name} from {self.team}, rank: {self.rank}'

    def get_url(self):
        return "https://playarena.pl/" + str(self.id) + ",profil_zawodnika,rozgrywek_amatorskich,index.html"


@app.route('/')
def index():
    ranked_players = Player.query.filter(Player.rank != 0).order_by(Player.rank).all()
    rest_players = Player.query.filter(Player.rank == 0).all()
    return render_template("index.html", players=ranked_players, rest_players=rest_players)


if __name__ == '__main__':
    app.run()
