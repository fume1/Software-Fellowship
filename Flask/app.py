from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# --------for image upload---------
# from werkzeug.utils import secure_filename
# import os

app = Flask(__name__)
# database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)
#---------image config--------
# UPLOAD_FOLDER = 'static/'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno}-{self.title}"


with app.app_context():
    db.create_all()


@app.route("/",methods=["GET","POST"])
def homo_todo():
    # allTodo = db.session.execute(db.select(Todo)).scalars().all()
    allTodo = Todo.query.all()
    if(request.method=="POST"):
        queryStr=request.form["search"]
        posts=Todo.query.filter(Todo.title.contains(queryStr)).all()
        print(posts)
        return render_template('index.html', allTodo=posts)


    return render_template('index.html', allTodo=allTodo)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/create-todo", methods=['GET', 'POST'])
def create_todo():
    if (request.method == "POST"):
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

        return redirect("/")


@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update_todo(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if (request.method == "POST"):
        title = request.form['title']
        desc = request.form['desc']
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()

        return redirect("/")
    return render_template('update.html', todo=todo)


@app.route("/delete/<int:sno>", methods=['GET'])
def delete_todo(sno):
    # todo = db.session.execute(db.select(Todo).filter_by(sno=sno)).scalar_one()
    todo = Todo.query.filter_by(sno=sno).first()
    print(todo)
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")




# --------homo_todo with handling files------------

# @app.route("/")
# def homo_todo():
#     # allTodo = db.session.execute(db.select(Todo)).scalars().all()
#     files = os.listdir(app.config['UPLOAD_FOLDER'])
#     images = []
#     for file in files:
#         print(file)
#         extension = allowed_file(file)
#         print(extension)
#         # extension = os.path.splitext(file.filename)[1]
#         # if extension in app.config['UPLOAD_FOLDER']:
#         images.append(file)
#     allTodo = Todo.query.all()
#     return render_template('index.html', allTodo=allTodo, images=images)


# ---------create_todo with handling files-------------
# @app.route("/create-todo", methods=['GET', 'POST'])
# def create_todo():
#     if (request.method == "POST"):
#         title = request.form['title']
#         desc = request.form['desc']
#         todo = Todo(title=title, desc=desc)
#         db.session.add(todo)
#         db.session.commit()
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             # return redirect("/")
#         return redirect("/")


# ------allowed files utils------------
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ------uploading files------------


# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('download_file', name=filename))


if __name__ == "__main__":
    app.run(debug=True)
