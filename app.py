from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)  # передает название этого файла
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class MyDateTime(db.TypeDecorator):
    impl = db.DateTime

    def process_bind_param(self, value, dialect):
        if type(value) is str:
            return datetime.datetime.strptime(value, '%Y-%m-%d')
        return value

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(300), nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    date = db.Column(MyDateTime, default=datetime.datetime.utcnow)
    age = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
#@app.route('/create-article', methods=['POST', 'GET'])
def index():
    return render_template("index.html")


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении возникла ошибка"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.first_name = request.form['first_name']
        article.last_name = request.form['last_name']
        article.diagnosis = request.form['diagnosis']
        #article.date = request.form['date']
        article.age = request.form['age']
        try:
           db.session.commit()    #save the object
           return redirect('/posts')
        except:
           return "При редактировании данных произошла ошибка"

    else:

        return render_template("post_update.html",article=article)



@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        diagnosis = request.form['diagnosis']
        date = request.form['date']
        age = request.form['age']

        article = Article(first_name=first_name, last_name=last_name, diagnosis=diagnosis, date=date, age=age)

        try:
            db.session.add(article)
            db.session.commit()    #save the object
            return redirect('/posts')
        except:
            return "При добавлении данных произошла ошибка"

    else:
        return render_template("create-article.html")


if __name__ == "__main__":
    app.run(debug=True)  #запустить локальный сервер