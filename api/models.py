from run import db
from package.global_variable.variables import tokens


class TokenModel(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    identity = db.Column(db.String(30), unique=True, nullable=False)
    jti = db.Column(db.String(100), unique=True, nullable=False)
    token = db.Column(db.String(500), nullable=False)
    date = db.Column(db.BigInteger, nullable=False)
    mode = db.Column(db.String(10), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_identity(cls, identity):
        return cls.query.filter_by(identity=identity).first()

    @classmethod
    def find_by_jti(cls, jti):
        return cls.query.filter_by(jti=jti).first()

    @classmethod
    def delete_by_jti(cls, jti):
        if cls.query.filter_by(jti=jti).delete():
            db.session.commit()
            return True
        return False

    @classmethod
    def switch_revoked(cls, jti):
        token = cls.find_by_jti(jti)
        if token:
            token.revoked = not token.revoked
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

    @staticmethod
    def return_all_jti_with_revoked():
        dict_jti_revoked = {}
        for x in TokenModel.query.all():
            dict_jti_revoked[f'{x.jti}'] = x.revoked
        return dict_jti_revoked


def update_token_in_memory():
    tokens.clear()
    for k, v in TokenModel.return_all_jti_with_revoked().items():
        tokens[k] = v
