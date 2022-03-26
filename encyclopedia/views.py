from django.shortcuts import render
from markdown2 import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = util.get_entry(title)
    if content is not None:
        entry_html = markdown(content)
    else:
        entry_html = "<h1>Error: Page Not Found</h1>"

    return render(request, "encyclopedia/entry.html", {"title": title, "entry": entry_html})
