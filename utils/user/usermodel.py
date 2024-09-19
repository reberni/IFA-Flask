from flask_login import UserMixin

def userModel(dbmodel):
    class Userstate(UserMixin, dbmodel):
        # Implement necessary methods required by Flask-Login

        def is_authenticated(self):
            """Return True if the user is authenticated."""
            return self.is_active

        def is_active(self):
            """Return True if the user is active."""
            return self.active

        def is_anonymous(self):
            """Return True if the user is anonymous."""
            return False

        def get_id(self):
            """Return the user ID as a unicode string."""
            return str(self.id)

        # Optionally, you can override the __repr__ method for better representation
        def __repr__(self):
            return f'<User {self.username}>'
    return Userstate