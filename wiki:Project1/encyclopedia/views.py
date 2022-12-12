import markdown
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util


# Main page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": SearchForm()
    })


# Entry page
def entry(request, title):
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/error.html", {
            "title": title.capitalize(),
            "search_form": SearchForm()
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown.markdown(util.get_entry(title)),
            "title": title.capitalize(),
            "search_form": SearchForm()
        })


# Making a search form
class SearchForm(forms.Form):
    query = forms.CharField(label="Search Encyclopedia", min_length=1)


# Search a query
# TODO: Make it a form and check whether it is valid that way (similar to lecture) then redirect to entry views
def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["query"]
            if util.get_entry(search):
                return render(request, "encyclopedia/entry.html", {
                    "entry": markdown.markdown(util.get_entry(search)),
                    "title": search.capitalize(),
                    "search_form": SearchForm()
                })
            elif len(util.get_similar(search)) > 0:
                return render(request, "encyclopedia/similar.html", {
                    "title": search.capitalize(),
                    "similar": util.get_similar(search),
                    "search_form": SearchForm()
                })
            else:
                return render(request, "encyclopedia/error.html", {
                    "title": search.capitalize(),
                    "search_form": SearchForm()
                })

    # If page is not valid or not posted, redirect to main page
    # return HttpResponseRedirect(reverse("encyclopedia:index.html"))
