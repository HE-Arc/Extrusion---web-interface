from package.global_variable.variables import tokens


def is_jti_blacklisted(jti):
    try:
        return tokens[jti]
    except:
        return True
