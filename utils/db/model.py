from sqlalchemy.orm import Mapped, mapped_column, relationship

def createDatabase(db, app):
    class User(db.Model):
        id: Mapped[int] = mapped_column(primary_key=True)
        username: Mapped[str] = mapped_column(db.String(50), unique=True)
        email: Mapped[str] = mapped_column(db.String(120))
        password: Mapped[str] = mapped_column(db.String(500), nullable=False)
        active: Mapped[bool] = mapped_column(db.Boolean, default=True)
        # One-to-Many relationship with Products
        products: Mapped[list] = relationship('Products', back_populates='creator')

    class Products(db.Model):
        id: Mapped[int] = mapped_column(primary_key=True)
        productname: Mapped[str] = mapped_column(db.String(50), unique=False)
        productdescription: Mapped[str] = mapped_column(db.String(500), unique=False)
        productprice: Mapped[int] = mapped_column(db.Integer, unique=False)
        productbrand: Mapped[str] = mapped_column(db.String(50), unique=False)
        # Foreign Key to link with User
        productcreator_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('user.id'))
        # Relationship to User
        creator: Mapped['User'] = relationship('User', back_populates='products')

    def initdb():
        with app.app_context():
            db.create_all()
    
    db.init_app(app)
    initdb()