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


def support(request):
    return render(
        request,
        'shared/support.html',
    )


def payment(request):
    return render(
        request,
        'shared/payment.html',
    )


def about_us(request):
    return render(
        request,
        'shared/about_us.html',
    )
