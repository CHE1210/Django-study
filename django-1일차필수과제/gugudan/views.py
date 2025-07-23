from django.shortcuts import render

def all_gugudan_view(request):
    # 예시 데이터 구조 (실제 코드는 다를 수 있어요)
    gugudans = [
        {'dan': i, 'lines': [f"{i} x {j} = {i*j}" for j in range(1, 10)]} for i in range(1, 10)
    ]
    return render(request, 'gugudan/all_gugudan.html', {'gugudans': gugudans})