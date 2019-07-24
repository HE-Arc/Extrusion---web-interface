from package.global_variable.variables import tokens


def is_jti_blacklisted(jti):
    """callback function of blacklist function

    :param jti: id of token
    :return: true if no active, false if active
    """
    try:
        return tokens[jti]
    except:
        return True
