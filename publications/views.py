from publications.models import Publication
from django.shortcuts import render_to_response

def latest(request):
    publication = Publication.objects.order_by('added')[0]
    context = {'publication': publication}
    return render_to_response('publications/latest.html', context)
