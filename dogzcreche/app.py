from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dogzcreche.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # This is just here to suppress a warning from SQLAlchemy as it will soon be removed
db = SQLAlchemy(app)                    # This is where we create the database object

class Dog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    owner = db.Column(db.String(100), nullable=False)
    owner_phone = db.Column(db.String(100), nullable=False)
    owner_email = db.Column(db.String(100))
    notes = db.Column(db.Text)


    def __repr__(self):
        return f'<Dog {self.name}>'

@app.route('/')
def index():
    dogs = Dog.query.all()  

    return render_template('index.html', dogs=dogs)


@app.route('/dog_detail/<int:id>')
def dog_detail(id):
    dog = Dog.query.get_or_404(id)
    return render_template('dog_detail.html', dog=dog)


@app.route('/add_new_dog', methods=['GET', 'POST'])
def add_new_dog():
    if request.method == 'POST':
        name = request.form['name']
        breed = request.form['breed']
        age = request.form['age']
        owner = request.form['owner']
        owner_phone = request.form['owner_phone']
        owner_email = request.form['owner_email']
        notes = request.form['notes']

        dog = Dog(name=name, breed=breed, age=age, owner=owner, owner_phone=owner_phone, owner_email=owner_email, notes=notes)
        db.session.add(dog)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('add_new_dog.html')

@app.route('/edit_dog_details/<int:id>', methods=['GET', 'POST'])
def edit_dog_details(id):
    dog = Dog.query.get_or_404(id)

    if request.method == 'POST':
        dog.name = request.form['name']
        dog.breed = request.form['breed']
        dog.age = request.form['age']
        dog.owner = request.form['owner']
        dog.owner_phone = request.form['owner_phone']
        dog.owner_email = request.form['owner_email']
        dog.notes = request.form['notes']

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_dog_details.html', dog=dog)

@app.route('/delete_dog/<int:id>')
def delete_dog(id):
    dog = Dog.query.get_or_404(id)
    db.session.delete(dog)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')




if __name__ == '__main__':
    app.run(debug=True)