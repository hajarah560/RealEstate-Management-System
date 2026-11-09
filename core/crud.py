"""Small helpers shared by every list / add / edit / delete view."""
from django.contrib import messages
from django.db.models import ProtectedError, Q
from django.http import HttpResponse
from django.shortcuts import render


def search(queryset, text, fields):
    """Keep rows where any of `fields` contains the text."""
    text = (text or "").strip()
    if not text:
        return queryset
    query = Q()
    for field in fields:
        query |= Q(**{field + "__icontains": text})
    return queryset.filter(query)


def list_context(request, queryset, search_fields, heading, add_url, add_label):
    q = request.GET.get("q", "").strip()
    return {
        "object_list": search(queryset, q, search_fields),
        "q": q,
        "heading": heading,
        "add_url": add_url,
        "add_label": add_label,
    }


def save_form(request, form_class, title, instance=None):
    """Add or edit. GET shows the form in the modal, a valid POST answers 204."""
    if request.method == "POST":
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            saved = form.save()
            messages.success(request, f"Saved: {saved}")
            return HttpResponse(status=204)
    else:
        form = form_class(instance=instance)
    return render(request, "shared/modal_form.html", {"form": form, "title": title, "action": request.path})


def remove(request, obj, title):
    """Delete. GET asks "are you sure?", POST deletes (unless something still uses it)."""
    error = ""
    if request.method == "POST":
        try:
            obj.delete()
        except ProtectedError:
            error = "This record is still used by a lease or payment, so it cannot be deleted."
        else:
            messages.success(request, f"Deleted: {obj}")
            return HttpResponse(status=204)
    return render(request, "shared/modal_confirm.html", {"title": title, "object": obj, "error": error, "action": request.path})
