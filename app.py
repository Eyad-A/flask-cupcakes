"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.route("/")
def show_index():
    """Show homepage"""

    return render_template("index.html")


@app.route("/api/cupcakes")
def show_cupcakes():
    """Return JSON of all cupcakes"""

    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)


@app.route("/api/cupcakes/<int:cupcake_id>")
def list_single_cupcake(cupcake_id):
    """Return JSON of a single cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.to_dict())


@app.route("/api/cupcakes", methods=["POST"]) 
def create_cupcake():
    """Create a cupcake from data and return it"""

    cupcake = Cupcake(
        flavor = request.json['flavor'],
        rating = request.json['rating'],
        size = request.json['size'],
        image = request.json['image'] or None
    )

    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.to_dict()), 201)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update a cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json['flavor']
    cupcake.rating = request.json['rating']
    cupcake.size = request.json['size']
    cupcake.image = request.json['image']

    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.to_dict()), 200)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Delete a cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")