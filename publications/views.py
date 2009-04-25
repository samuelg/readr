from publications.models import Publication, Reading
from django.shortcuts import render_to_response
from publications.forms import PublicationForm, ReadingForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage


def latest(request):
    publication_list = Publication.objects.order_by('-added')
    readings = []

    # setup pagination
    paginator = Paginator(publication_list, 2)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        publications = paginator.page(page)
    except (EmptyPage, InvalidPage):
        publications = paginator.page(paginator.num_pages)

    for publication in publications.object_list:
        try:
            if not request.user.is_authenticated():
                raise Reading.DoesNotExist
            reading = Reading.objects.get(publication=publication, user=request.user)
        except Reading.DoesNotExist:
            readings.append(None)
        else:
            readings.append(reading)

    # store publication objects and associated reading objects in a tupple
    publications.object_list = zip(publications.object_list, readings)

    reading_form = ReadingForm()    
    context = {'publications': publications, 'reading_form': reading_form}

    return render_to_response('publications/latest.html',
        context,
        context_instance=RequestContext(request)
    )

@login_required
def create(request):
    form = PublicationForm(request.POST or None)

    if form.is_valid():
        publication = form.save(commit=False)
        publication.owner = request.user
        publication.save()
        request.user.message_set.create(message='Publication created')

        return HttpResponseRedirect(request.POST.get('next', reverse('pub_latest')))

    return render_to_response('publications/create.html',
        {'form': form},
        context_instance=RequestContext(request)
    )

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

        return HttpResponseRedirect(request.POST.get('next', reverse('pub_latest')))

    return render_to_response('publications/view.html',
        {'publication': publication, 'reading_form': form},
        context_instance=RequestContext(request)
    )

def view(request, publication_id):
    form = ReadingForm()
    reading = None

    try:
        publication = Publication.objects.get(id=publication_id)
    except Publication.DoesNotExist:
        return Http404

    try:
        if not request.user.is_authenticated():
            raise Reading.DoesNotExist
        reading = Reading.objects.get(publication=publication, user=request.user)
    except Reading.DoesNotExist:
        pass

    return render_to_response('publications/view.html',
        {'publication': publication, 'reading': reading, 'reading_form': form},
        context_instance=RequestContext(request)
    )
