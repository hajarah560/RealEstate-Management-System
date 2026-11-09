from django.db.models import Q


# Keep only the rows where any of the given fields contains the search text
def search(queryset, text, fields):
    text = (text or "").strip()
    if not text:
        return queryset
    query = Q()
    for field in fields:
        query |= Q(**{field + "__icontains": text})
    return queryset.filter(query)
