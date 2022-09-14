from datetime import datetime
from .sqlInteraction import SQLInteractor


def datetimeValid(dt_str):
    try:
        datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    except Exception:
        return False

    return True


def parentValid(i):
    if SQLInteractor().getParentType(i) == 'FILE':
        return False
    if SQLInteractor().getElement(i)['type'] == 'FILE':
        if SQLInteractor().getChildren(i):
            return False

    return True


def urlValid(i):
    el = SQLInteractor().getElement(i)
    if el['type'] == 'FOLDER':
        if not el['url']:
            return True
    else:
        if not el['url']:
            return False
        elif 1 <= len(el['url']) <= 255:
            return True

    return False


def sizeValid(i):
    el = SQLInteractor().getElement(i)
    if el['type'] == 'FOLDER':
        if not el['size']:
            return True
    else:
        if not el['size']:
            return False
        elif el['size'] > 0:
            return True

    return False


def typeValid(i):
    el = SQLInteractor().getElement(i)
    if el['type'] == 'FILE' or el['type'] == 'FOLDER':
        return True
    return False


def inputValid(ids):
    for i in ids:
        if typeValid(i) and sizeValid(i) and parentValid(i) and urlValid(i):
            continue
        else:
            return False
    return True
