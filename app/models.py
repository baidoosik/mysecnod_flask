from . import db

class Role(db.Model):
    __tablename__ = 'roles'
    id =  db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship('User',backref='role')

    def __repr__(self):
        return '<Role {}>'.format(self.name)

class User(db.Model):
    __tablename__ = 'users'
    id= db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(40),unique=True,index=True)
    email = db.Column(db.String(60))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<USER {}>'.format(self.user_name)