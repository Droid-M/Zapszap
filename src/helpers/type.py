import json

def is_json_string(variable):
    try:
        json.loads(variable)
        return True
    except (json.JSONDecodeError, TypeError):
        return False
    except UnicodeDecodeError as e:
        return False