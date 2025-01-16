from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import get_etherscan_transactions, get_crypto_prices


logger = logging.getLogger('django')

def test_logging(request):
    logger.debug("Test log message")
    return JsonResponse({"message": "Logged"})


@api_view(['GET'])
def transactions(request):
    address = request.query_params.get('address')
    if not address:
        return Response({"error": "Address is required"}, status=400)
    data = get_etherscan_transactions(address)
    return Response(data)

@api_view(['GET'])
def prices(request):
    symbol = request.query_params.get('symbol')
    if not symbol:
        return Response({"error": "Symbol is required"}, status=400)
    data = get_crypto_prices(symbol)
    return Response(data)
