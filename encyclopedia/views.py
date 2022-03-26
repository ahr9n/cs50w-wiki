from random import choice

from django.shortcuts import render, redirect
from markdown2 import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, title):
    content = util.get_entry(title.strip())
    if content is None:
        content = "<h1>Error: Page Not Found</h1>"
    content = markdown(content)
    return render(request, "encyclopedia/entry.html", {"title": title, "entry": content})


def search(request):
    q = request.GET.get('q').strip()
    if q in util.list_entries():
        return redirect("entry", title=q)
    return render(request, "encyclopedia/search.html", {"entries": util.search(q), "q": q})


def create(request):
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
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/edit.html", {"error": "Page not found!"})
    if request.method == "POST":
        content = request.POST.get("content").strip()
        if content == "":
            return render(request, "encyclopedia/edit.html", {"error": "Content is required!"})
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/edit.html", {"title": title, "content": content})


def random(request):
    entries = util.list_entries()
    return redirect("entry", title=choice(entries))

