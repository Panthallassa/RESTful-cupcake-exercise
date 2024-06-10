"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template
from models import db, connect_db, serialize_cupcake, Cupcake


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


with app.app_context():
    connect_db(app)


@app.route('/', methods=["GET"])
def index():
    """Render the HTML page"""

    return render_template('index.html')


@app.route('/api/cupcakes', methods=["GET"])
def list_cupcakes():
    """Return JSON of cupcakes"""

    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(c) for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.route('/api/cupcakes/<int:id>', methods=["GET"])
def show_cupcake(id):
    """Get data about a single cupcake by ID"""

    cupcake = Cupcake.query.get_or_404(id)

    return jsonify(cupcake=serialize_cupcake(cupcake))

@app.route('/api/cupcakes', methods={"POST"})
def create_cupcake():
    """Create a new cupcake"""

    data = request.json

    flavor = data.get('flavor')
    size = data.get('size')
    rating = data.get('rating')
    image = data.get('image', 'https://tinyurl.com/demo-cupcake')

    if not (flavor and size and rating):
        return jsonify(error='Missing required fields'), 400
    
    cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=serialize_cupcake(cupcake)), 201


@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    """Updates a cupcake by id"""

    cupcake = Cupcake.query.get_or_404(id)

    data = request.json

    cupcake.flavor = data.get('flavor', cupcake.flavor)
    cupcake.size = data.get('size', cupcake.size)
    cupcake.rating = data.get('rating', cupcake.rating)
    cupcake.image = data.get('image', cupcake.image)

    db.session.commit()

    serialized_cupcake = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized_cupcake)


@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    """Deletes a cupcake by id"""

    cupcake = Cupcake.query.get_or_404(id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message='Deleted Cupcake')

