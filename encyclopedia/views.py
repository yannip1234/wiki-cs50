from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import random

from . import util
import markdown2


class NewTopicForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea)


class NewEditForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def search(request):
    if request.method == "POST":

        entries = util.list_entries()
        query = request.POST.get('q')
        results = []
        for entry in entries:
            if query.lower() in entry.lower():
                results.append(entry)
        return render(request, "encyclopedia/results.html", {
            "query": query,
            "results": results
        })


def edit(request, entrytitle):
    existingcontent = util.get_entry(entrytitle)
    form = NewEditForm({"title": entrytitle, "content": existingcontent})
    if request.method == "POST":
        form = NewEditForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            f = open("entries/" + title + ".md", "w")
            f.write(content)
            f.close()
            return HttpResponseRedirect("/" + title)
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    return render(request, "encyclopedia/edit.html", {
        "form": form
    })


def randompage(request):
    chosenpage = random.choice(util.list_entries())
    return HttpResponseRedirect("/" + chosenpage)



def getentry(request, entryname):
    return render(request, "encyclopedia/entry.html", {
            "entrytitle": entryname,
            "entries": markdown2.markdown(util.get_entry(entryname))
    })


def create(request):
    if request.method == "POST":
        form = NewTopicForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            try:
                f = open("entries/" + title + ".md", "x")
                f.write(content)
                f.close()
            except OSError:
                return render(request, "encyclopedia/create.html", {
                    "form": "Error. File exists."
                })
            return HttpResponseRedirect("/"+title)
        else:
            return render(request, "encyclopedia/create.html", {
               "form": form
           })

    return render(request, "encyclopedia/create.html", {
        "form": NewTopicForm()
    })

