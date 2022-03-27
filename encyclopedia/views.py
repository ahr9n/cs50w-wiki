from random import choice

from django.shortcuts import render, redirect
from markdown2 import markdown

from . import util


def index(request):
    """ Home Page, displays all available entries """
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, title):
    """ Displays the requested entry """
    content = util.get_entry(title.strip())
    if content is None:
        content = "<h1>Error: Page Not Found</h1>"
    content = markdown(content)
    return render(request, "encyclopedia/entry.html", {"title": title, "entry": content})


def search(request):
    """ Loads requested title page if it exists, else displays search results """
    q = request.POST.get('q').strip()
    if q in util.list_entries():
        return redirect("entry", title=q)
    return render(request, "encyclopedia/search.html", {"entries": util.search(q), "q": q})


def create(request):
    """ Lets users create a new page on the wiki """
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()
        if title in util.list_entries():
            return render(request, "encyclopedia/create.html", {"error": "Page already exists!"})
        elif title == "" or content == "":
            return render(request, "encyclopedia/create.html", {"error": "Title and content are required!"})
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/create.html")


def edit(request, title):
    """ Lets users edit an existing page on the wiki """
    content = util.get_entry(title.strip())
    if content is None:
        return render(request, "encyclopedia/edit.html", {'error': "Page Not Found"})
    if request.method == "GET":
        content = request.GET.get("content").strip()
        if content == "":
            return render(request, "encyclopedia/edit.html",
                          {"message": "Can't save with empty field.", "title": title, "content": content})
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/edit.html", {'content': content, 'title': title})


def random(request):
    """ Loads a random page from the wiki """
    entries = util.list_entries()
    return redirect("entry", title=choice(entries))
