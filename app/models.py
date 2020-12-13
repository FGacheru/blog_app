from . import db


class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_secure = db.Column(db.String(255))
    
    pitch = db.relationship('Comments', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'User {self.username}'
    
    pass_secure  = db.Column(db.String(255))

    @property
    def password(self):
            raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
            self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
            return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'
    
    
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}
    
    
class Views(db.Model):
    __tablename__ = 'views'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    opinion_title = db.Column(db.String(255), index=True)
    description = db.Column(db.String(255), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    

    def save_views(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_views(cls, id):
        views = Post.query.filter_by(id=id).all()
        return views

    @classmethod
    def get_all_views(cls):
        views = Views.query.order_by('-id').all()
        return views

    def __repr__(self):
        return f'Posts {self.views_title}'
    
    
class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime(250), default=datetime.utcnow)
    views_id = db.Column(db.Integer, db.ForeignKey("views.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comment(cls,id):
        comments = Comments.query.filter_by(views_id=id).all()
        return comments
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()    

    def __repr__(self):
        return f"Comments('{self.comment}', '{self.date_posted}')"
    
    