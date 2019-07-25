from run import db
from package.global_variable.variables import tokens


class TokenModel(db.Model):
    """Represents The table token in db

    """
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    identity = db.Column(db.String(200), unique=True, nullable=False)
    jti = db.Column(db.String(100), unique=True, nullable=False)
    token = db.Column(db.String(500), nullable=False)
    date = db.Column(db.BigInteger, nullable=False)
    mode = db.Column(db.String(10), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)

    def save_to_db(self):
        """Commit model object to create table in db

        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_identity(cls, identity):
        """find a token with his identity in db

        :param identity: identity of token to find
        """
        return cls.query.filter_by(identity=identity).first()

    @classmethod
    def find_by_jti(cls, jti):
        """find a token in db with his jti

        :param jti: jti of token to find
        """
        return cls.query.filter_by(jti=jti).first()

    @classmethod
    def delete_by_jti(cls, jti):
        """delete a token in db

        :param jti:
        :return:
        """
        if cls.query.filter_by(jti=jti).delete():
            db.session.commit()
            return True
        return False

    @classmethod
    def switch_revoked(cls, jti):
        """Change revoked status in db

        :param jti: jti of token to change revoke status
        :return:
        """
        token = cls.find_by_jti(jti)
        if token:
            token.revoked = not token.revoked
            db.session.commit()
            return True
        return False

    @staticmethod
    def return_all():
        """return all token information

        :return: json representation of table token
        """
        # in app it is not revoked but activate, so switch revoked information
        def to_json(x):
            return {
                'jti': x.jti,
                'identity': x.identity,
                'mode': x.mode,
                'date': x.date,
                'active': not x.revoked,
                'token': x.token
            }

        return {'tokens': list(map(lambda x: to_json(x), TokenModel.query.all()))}

    @staticmethod
    def return_all_jti_with_revoked():
        """ create a dictionary of token with is revoked status

        :return: dict with key:jti, value: revoked Status
        """
        dict_jti_revoked = {}
        for x in TokenModel.query.all():
            dict_jti_revoked[f'{x.jti}'] = x.revoked
        return dict_jti_revoked


def update_token_in_memory():
    """ Update the global variable of all token with value in db

    """
    tokens.clear()
    for k, v in TokenModel.return_all_jti_with_revoked().items():
        tokens[k] = v
