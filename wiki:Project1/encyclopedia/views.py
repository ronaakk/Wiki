import markdown
from django import forms
from django.contrib import messages
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


# Search a query

# Making a search form
class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Search Encyclopedia'}), min_length=1, label="")


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
                    "title": search,
                    "similar": util.get_similar(search),
                    "search_form": SearchForm()
                })
            else:
                return render(request, "encyclopedia/error.html", {
                    "title": search,
                    "search_form": SearchForm()
                })

    # If page is not valid or not posted, redirect to main page
    return HttpResponseRedirect(reverse("encyclopedia:index"))


# Creating a new Page

# Making a new page form
class NewPageForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
        "placeholder": "Page Title"}))
    content = forms.CharField(label='', widget=forms.Textarea(attrs={
        "placeholder": "Enter Page Content using Github Markdown"
    }))


def create(request):

    # When the link in the navbar is clicked, load the form
    if request.method == "GET":
        return render(request, "encyclopedia/create.html", {
            "create_form": NewPageForm(),
            "search_form": SearchForm()
        })

    # When save button is hit
    elif request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            new_entry = form.cleaned_data["title"]
            new_content = form.cleaned_data["content"]
            # If the title already exists
            if util.get_entry(new_entry):
                messages.error(request,
                               "Oops! A encyclopedia with this name already exists. Choose a different name or edit the one that currently exists!")
                return render(request, "encyclopedia/create.html", {
                    "search_form": SearchForm(),
                    "create_form": form
                })
            else:
                # Save the entry otherwise
                util.save_entry(new_entry, new_content)
                messages.success(request,
                                 f"New page: '{new_entry}' created successfully!")
                return render(request, "encyclopedia/entry.html", {
                    "title": new_entry.capitalize(),
                    "search_form": SearchForm(),
                    "entry": markdown.markdown(util.get_entry(new_entry))
                })
    else:
        # In the case the user did not provide a valid title
        messages.error(request, "Entry form not valid, please try again!")
        return render(request, "encyclopedia/create.html", {
            "create_form": form
        })
