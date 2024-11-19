from django.http import JsonResponse
from .models import LaunchedOffer
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from django.contrib.auth.decorators import login_required



def get_all_offers(request):
    offers = LaunchedOffer.objects.all()
    offers_json = serializers.serialize('json', offers)
    return JsonResponse({"offers": offers_json})


@login_required
@csrf_exempt
def update_offer(request, offer_id):
    data = json.loads(request.body)
    LaunchedOffer.objects.filter(id=offer_id).update(**data)
    return JsonResponse({"message": "Offer updated successfully"})

@csrf_exempt
def delete_offer(request, offer_id):
    LaunchedOffer.objects.filter(id=offer_id).delete()
    return JsonResponse({"message": "Offer deleted successfully"})


def get_offer(request, offer_id):
    try:
        offer = LaunchedOffer.objects.get(id=offer_id)
        offer_json = serializers.serialize('json', [offer])
        return JsonResponse({"offer": offer_json})
    except LaunchedOffer.DoesNotExist:
        return JsonResponse({"error": "Offer not found"}, status=404)
