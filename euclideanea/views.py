from django.shortcuts import render
from .extendedea import extendedEA

# Create your views here.
def index(request):
    return render(request, 'euclidean/index.html')

def calculate(request):
    if (request.method == 'POST'):
        try:
            a = int(request.POST.get('a'))
            b = int(request.POST.get('b'))
        except (TypeError, ValueError):
            return render(request, 'euclidean/index.html', {'error': 'Please enter valid integers.'})
        if (abs(a) > abs(b)):
            r1 = a
            r2 = b
        else:
            r2 = a
            r1 = b

        gcd, x, y, steps = extendedEA(r1, r2, 1, 0, 0, 1)
        context = {
            'a' : r1, 
            'b' : r2, 
            'gcd' : gcd, 
            'x' : x, 
            'y' : y,
            'steps' : steps,
            'result_calculated' : True,
        }
        return render(request, 'euclidean/index.html', context)
    return render(request, 'euclidean/index.html')