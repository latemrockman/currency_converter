from django.shortcuts import render
import requests
import json


# Create your views here.


def exchange(request):
    # response = requests.get(url='https://api.exchangerate-api.com/v4/latest/USD')
    API_KEY = 'AgdCeFPnv5JF8ormBZYOnqn7u7h4OB8nXV74FwfM'
    currencyapi = requests.get(url=f'https://api.currencyapi.com/v3/latest?apikey={API_KEY}')
    resp = json.loads(currencyapi.content)['data']
    meta = json.loads(currencyapi.content)['meta']['last_updated_at']
    day = meta[8:10]
    month = meta[5:7]
    year = meta[:4]
    time = meta[-9:-1]
    meta_up = f'{time} {day}.{month}.{year}'

    all_currencies = [cur for cur in resp.keys()]

    context = {
        'currencies': all_currencies,
        'meta_up': meta_up
    }

    if request.method == "GET":
        return render(request, 'exchange_app/index.html', context)

    if request.method == 'POST':
        from_amount = float(request.POST['from-amount'])
        from_curr = request.POST.get('from-curr')
        to_curr = request.POST.get('to_curr')

        from_value = resp[from_curr]['value']
        to_value = resp[to_curr]['value']

        converted_amount = round((to_value / from_value) * float(from_amount), 2)

        context['from_amount'] = from_amount
        context['to_curr'] = to_curr
        context['from_curr'] = from_curr
        context['converted_amount'] = converted_amount

        return render(request, 'exchange_app/index.html', context)

    return render(request, 'exchange_app/index.html', context)
