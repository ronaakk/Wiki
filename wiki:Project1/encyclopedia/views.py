from django.shortcuts import render

from . import util

# Write your views here.


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Entry page


def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "title": util.get_entry(title)
    })
