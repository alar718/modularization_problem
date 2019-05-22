from flask import render_template, request, redirect
from sqlalchemy.sql import func
from config import app, db

class Dojo(db.Model):
    __tablename__ = "dojos"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, server_default = func.now())
    updated_at = db.Column(db.DateTime, server_default = func.now(), onupdate = func.now())

class Ninja(db.Model):
    __tablename__ = "ninjas"
    id = db.Column(db.Integer, primary_key = True) # autoincremented id
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    # dojo = db.Column(db.String(100))
    school_id = db.Column(db.Integer, db.ForeignKey('dojos.id'), nullable = False)
    school = db.relationship('Dojo', foreign_keys = [school_id], backref="dojo_students", cascade="all")
    created_at = db.Column(db.DateTime, server_default = func.now())
    updated_at = db.Column(db.DateTime, server_default = func.now(), onupdate = func.now())

@app.route("/")
def main():
    dojo_list = Dojo.query.all()
    ninja_list = Ninja.query.all()
    return render_template("main.html", dojos = dojo_list, ninjas = ninja_list)

@app.route('/addDojo', methods=['POST'])
def add_dojo():
    new_dojo = Dojo(
        name = request.form['thename'],
        city = request.form['thecity'],
        state = request.form['thestate']
    )
    db.session.add(new_dojo)
    db.session.commit()
    return redirect('/')

@app.route('/addNinja', methods=['POST'])
def add_ninja():
    new_ninja = Ninja(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        school_id = int(request.form['selectz'])
    )
    db.session.add(new_ninja)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)