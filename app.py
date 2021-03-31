from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    oll_rating = db.Column(db.String(32), default='?')
    dee_rating = db.Column(db.String(32), default='?')
    year = db.Column(db.Integer)

    def __init__(self, name, oll_rating, dee_rating, year):
        self.name = name
        self.oll_rating = oll_rating
        self.dee_rating = dee_rating
        self.year = year 


class MovieSchema(ma.Schema):
    class Meta: 
        fields = ('id', 'name', 'oll_rating', 'dee_rating', 'year')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


class MovieManager(Resource):
    @staticmethod
    def get():
        try: id = request.args['id']
        except Exception as _: id = None

        if not id:
            movies = Movie.query.all()
            return jsonify(movies_schema.dump(movies))
        movie = Movie.query.get(id)
        return jsonify(movie_schema.dump(movie))

    @staticmethod
    def post():
        name = request.json['name']
        year = request.json['year']
        oll_rating = "?";
        dee_rating = "?";
        movie = Movie(name, oll_rating, dee_rating, year)
        db.session.add(movie)
        db.session.commit()
        return jsonify({
           'Message': f'Movie {name} {year} inserted.'
        })

    @staticmethod
    def put():
        try: id = request.args['id']
        except Exception as _: id = None
        if not id:
            return jsonify({ 'Message': 'Must provide the movie ID' })
        movie = Movie.query.get(id)
        
        oll_rating = request.json['oll_rating']
        dee_rating = request.json['dee_rating']

        movie.oll_rating = oll_rating 
        movie.dee_rating = dee_rating

        db.session.commit()
        return jsonify({
            'Message': f'Movie {movie.name} {movie.year} rated.'
        })


api.add_resource(MovieManager, '/api/movies')

if __name__ == '__main__':
    app.run(debug=True)
