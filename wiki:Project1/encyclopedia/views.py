import markdown
from django.shortcuts import render

from . import util

# Main page


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Entry page

def entry(request, title):
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/error.html", {
            "title": title.capitalize()
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown.markdown(util.get_entry(title)),
            "title": title.capitalize()
        })


# Search a query

def search(request, query):
    if util.get_entry(query):
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown.markdown(util.get_entry(query)),
            "title": query.capitalize()
        })
    elif len(util.get_similar(query)) > 0:
        return render(request, "encyclopedia/similar.html", {
            # Do I need to pass entry?
            # "entry": markdown.markdown(util.get_entry(query)),
            "title": query.capitalize(),
            "similar": util.get_similar(query)
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "title": query.capitalize()
        })
