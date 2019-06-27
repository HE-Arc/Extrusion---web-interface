from package.global_variable.variables import tokens


def is_jti_blacklisted(jti):
    print(tokens)
    try:
        return tokens[jti]
    except:
        return True
