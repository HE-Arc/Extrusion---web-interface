from run import db


class TokenModel(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    identity = db.Column(db.String(30), unique=True, nullable=False)
    jti = db.Column(db.String(100), unique=True, nullable=False)
    token = db.Column(db.String(500), nullable=False)
    date = db.Column(db.BIGINT, nullable=False)
    mode = db.Column(db.String(10), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_identity(cls, identity):
        return cls.query.filter_by(identity=identity).first()

    @classmethod
    def delete_by_id(cls, identity):
        if cls.query.filter_by(identity=identity).delete():
            db.session.commit()
            return True
        return False

    @staticmethod
    def return_all():
        def to_json(x):
            return {
                'jit': x.jti,
                'identity': x.identity,
                'mode': x.mode,
                'date': x.date,
                'revoked': x.revoked,
                'token': x.token
            }

        return {'tokens': list(map(lambda x: to_json(x), TokenModel.query.all()))}
