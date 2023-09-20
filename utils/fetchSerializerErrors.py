def fetch_serializer_error(errors):
    try:
        error = [elem[0] for elem in errors.values()][0].capitalize()
        if 'Invalid pk' in error:
            error = list(errors.keys())[0].capitalize() + ' Does not Exist!'
        elif 'This field' in error:
            key = list(errors.keys())[0].capitalize()
            error = key + ' is required.'
        return error
    except:
        return None


