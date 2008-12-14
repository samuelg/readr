from publications.models import Publication, Reading
from django.shortcuts import render_to_response
from publications.forms import PublicationForm, ReadingForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required

def latest(request):
    publications = Publication.objects.order_by('-added')
    reading_form = ReadingForm()    
    context = {'publications': publications, 'reading_form': reading_form}
    return render_to_response('publications/latest.html', context)

@login_required
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

@login_required
def read(request, publication_id):
    form = ReadingForm(request.POST or None)
    try:
        publication = Publication.objects.get(id=publication_id)
    except Publication.DoesNotExist:
        return Http404
    if form.is_valid():
        reading = form.save(commit=False)
        reading.user = request.user
        reading.publication = publication
        reading.save()
        request.user.message_set.create(message='%s read' % (publication.title))
        if 'next' in request.POST:
            next = request.POST['next']
        else:
            next = reverse('pub_latest')
        return HttpResponseRedirect(next)
    return render_to_response('publications/view.html', {'publication': publication, 'reading_form': form})
