from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    desc=db.Column(db.String(500), nullable=False)
    date_created=db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno}-{self.title}"
    
with app.app_context():
    db.create_all()


@app.route("/",methods=['GET', 'POST'])
def hello_world():
    allTodo=Todo.query.all()
    if(request.method == "POST"):
        search=request.form["search"]
        todos=Todo.query.filter(Todo.title.contains(search)).all()
        return render_template('index.html',allTodo=todos)


    # todo=Todo(title="Ram",desc="This is desc")
    # db.session.add(todo)
    # db.session.commit()
    return render_template("index.html",allTodo=allTodo)


@app.route("/create-todo",methods=["GET","POST"])
def create_todo():
    if(request.method == "POST"):
        title=request.form['todo']
        # passing that name in big brackets which is shown to us in other side.
        desc=request.form['description']
        print(title)
        todo=Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    return redirect("/") 
# this means that everything i have wrote above is to be returned to my webpage that is /

@app.route("/update/<int:sno>",methods=["GET","POST"])
def update_todo(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    if(request.method == "POST"):

        title=request.form['todo']
        # passing that name in big brackets which is shown to us in other side.
        desc=request.form['description']
        todo.title=title
        todo.desc=desc
        # todo=Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    return render_template("update.html", todo=todo) 

@app.route('/show')
def show():
    allTodo=Todo.query.all()
    print(allTodo)
    return"This is shown"

@app.route("/delete/<int:sno>",methods=['GET'])
def delete_todo(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    # the front sno is from above sno i.e line 10 while the back sno is from the parameter.
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


if __name__=="__main__":
    app.run(debug=True)