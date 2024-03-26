from sqlalchemy.orm import Mapped, mapped_column

def createDatabase(db, app):
    class User(db.Model):
        id: Mapped[int] = mapped_column(primary_key=True)
        username: Mapped[str] = mapped_column(db.String(50),unique=True)
        email: Mapped[str] = db.Column(db.String(120))
        password = db.Column(db.String(500), nullable=False)
        active = db.Column(db.Boolean, default=True)

    def initdb():
        with app.app_context():
            db.create_all()
    
    db.init_app(app)
    initdb()