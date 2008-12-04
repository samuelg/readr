from publications.models import Publication
from django.shortcuts import render_to_response
from publications.forms import PublicationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

def latest(request):
    publication = Publication.objects.order_by('-added')[0]
    context = {'publication': publication}
    return render_to_response('publications/latest.html', context)

def create(request):
    form = PublicationForm(request.POST or None)
    if form.is_valid():
        publication = form.save(commit=False)
        publication.owner = request.user
        publication.save()
        request.user.message_set.create(message='Publication created')
        if 'next' in request.POST:
            next = request.POST['next']
        else:
            next = reverse('pub_latest')
        return HttpResponseRedirect(next)
    return render_to_response('publications/create.html', {'form': form})
