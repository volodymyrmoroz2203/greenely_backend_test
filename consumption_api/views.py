from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET

from consumption_api.models import Days, Months
from consumption_api.utils import is_date_valid, is_count_valid, get_limits_dict, get_date_from_datetime, get_end_date


@login_required
@require_GET
def get_data(request):
    """
    Get data for current user
    :param request: start_date: start date of data set, count: amount of days or months,
    resolution: months or days (M or D)
    :return: JsonResponse with data
    """
    # get data from request
    user_id = request.user.id
    start_date = request.GET.get('start')
    count = request.GET.get('count')
    resolution = request.GET.get('resolution')

    # not all required fields are in request
    if not all([start_date, count, resolution]):
        return HttpResponseBadRequest('"start_date", "count" and "resolution" are required.')

    # check if date is valid
    if not is_date_valid(start_date):
        return HttpResponseBadRequest(f'Start date {start_date} is not valid. Please provide it in format: %Y-%m-%d.')

    # check if count is valid
    if not is_count_valid(count):
        return HttpResponseBadRequest(f'Count {count} is not valid. Please provide it as positive integer.')
    else:
        count = int(count)

    result = {'data': []}

    # make the list of entities according to resolution type.
    if resolution.lower() == 'd':
        end_date = get_end_date(start_date, count, 'd')
        stats = Days.objects.filter(
            user_id=user_id, timestamp__gte=start_date, timestamp__lt=end_date).order_by('timestamp')
    elif resolution.lower() == 'm':
        end_date = get_end_date(start_date, count, 'm')
        stats = Months.objects.filter(
            user_id=user_id, timestamp__gte=start_date, timestamp__lt=end_date).order_by('timestamp')
    else:
        return HttpResponseBadRequest('Resolution should be "M" (month) or "D" (day).')

    for entity in stats:
        result['data'].append([get_date_from_datetime(entity.timestamp), entity.consumption, entity.temperature])

    return JsonResponse(result)


@login_required
@require_GET
def get_limits(request):
    """
    Get limits for current user
    :param request:
    :return: JsonResponse with data
    """
    # get user id form request
    user_id = request.user.id

    # get limits for user and fill result dict
    limits = {'months': {}, 'days': {}}

    days_stats = Days.objects.filter(user_id=user_id)
    limits['days'] = get_limits_dict(days_stats)

    months_stats = Months.objects.filter(user_id=user_id)
    limits['months'] = get_limits_dict(months_stats)

    return JsonResponse(limits)
