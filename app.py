from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
db.init_app()
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


@app.route('/')
def index():
    players = Player.query.all()
    return render_template("index.html", players=players)


if __name__ == '__main__':
    app.run()
