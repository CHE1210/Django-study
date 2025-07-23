from django.shortcuts import render

def gugudan_all(request):
    gugudans = [
        {'dan': dan, 'lines': [f"{dan} x {i} = {dan * i}" for i in range(1, 10)]}
        for dan in range(1, 10)
    ]
    return render(request, 'gugudan_all.html', {'gugudans': gugudans})