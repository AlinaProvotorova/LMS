from django.shortcuts import render


def index(request):
    return render(
        request,
        'shared/index.html',
    )


def documents(request):
    return render(
        request,
        'shared/documents.html',
    )
