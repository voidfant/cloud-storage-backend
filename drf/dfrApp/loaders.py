from .serializers import *
from .validators import *
from .sqlInteraction import *


def processData(data: dict):
    ids = []
    if not datetimeValid(data['updateDate']):
        print('datetime trouble')
        return 400

    for item in data['items']:
        item['date'] = data['updateDate']
        if SQLInteractor().checkId(item['id']):
            serial = UpdateElementSerializer(data=item)
            if not serial.is_valid():
                print(serial.errors)
                return ''
            continue

        serial = ElementsDetailSerializer(data=item)
        if not serial.is_valid():
            print(serial.errors)
            return ""

    for item in data['items']:
        ids += [item['id']]
        if SQLInteractor().checkId(item['id']):
            SQLInteractor().updateDateOnInteraction(item['id'], item['date'])
            print(item['date'])
            SQLInteractor().updateElement(item)

            continue

        serial = ElementsDetailSerializer(data=item)
        if not serial.is_valid():
            print(serial.errors)
            return ""
        serial.save()
        SQLInteractor().updateDateOnInteraction(item['id'], item['date'])

    if inputValid(ids):
        return 200
    else:
        SQLInteractor().deleteElement(ids)
        return 400


def loadChildren(parentId: str):

    element = SQLInteractor().getElement(parentId)
    children = SQLInteractor().getChildren(parentId)
    if element['type'] == 'FILE':
        return element
    elif not children:
        element['children'] = []
        return element
    element['children'] = children
    for k, el in enumerate(element['children']):
        ch = loadChildren(el['id'])
        if el['type'] == 'FILE':
            element['children'][k]['children'] = None
            continue
        elif not ch:
            element['children'][k]['children'] = []
            continue
        element['children'][k]['children'] = ch['children']

    return element


