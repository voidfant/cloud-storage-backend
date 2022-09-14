from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .sqlInteraction import SQLInteractor
from .loaders import *
# Create your views here.


@api_view(['POST'])
def importApi(request, id=0):
    element_data = JSONParser().parse(request)
    try:
        if processData(element_data) == 200:
            return Response(status=200)
    except:
        return Response({"code": 400, "message": "Validation Failed"}, status=400)

    return Response({"code": 400, "message": "Validation Failed"}, status=400)


@api_view(['GET'])
def nodesApi(request, elementId, id=0):
    print(elementId)
    if not elementId:
        return Response({"code": 400, "message": "Validation Failed"}, status=400)
    if not SQLInteractor().checkId(elementId):
        return Response({"code": 404, "message": "Item not found"}, status=404)
    SQLInteractor().getFolderSize(elementId)
    result = loadChildren(elementId)

    return Response(result, status=200)


@api_view(['DELETE'])
def deleteApi(request, elementId, id=0):
    date = request.query_params.get('date')
    print(date)
    if not SQLInteractor().checkId(elementId):
        return Response({"code": 404, "message": "Item not found"}, status=404)
    if not datetimeValid(date):
        return Response({"code": 400, "message": "Validation Failed"}, status=400)
    ids = SQLInteractor().getChildrenIds(elementId)
    SQLInteractor().updateDateOnInteraction(elementId, date)
    SQLInteractor().deleteElement(ids)

    return Response(status=200)

