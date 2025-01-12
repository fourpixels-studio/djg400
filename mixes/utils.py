import json
from .models import Mix
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def update_download_count(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            mix_id = data.get('mix_id')
            mix = Mix.objects.get(id=mix_id)
            mix.download_count += 1
            mix.save()
            return JsonResponse({'success': True})
        except Mix.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Mix not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
