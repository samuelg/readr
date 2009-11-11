from publications.models import Publication, Reading, Quote
from django.shortcuts import render_to_response
from publications.forms import PublicationForm, ReadingForm, QuoteForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.models import User


def latest(request):
    """
        Displays the latest publications. Uses pagination.
    """
    return get_reads(request, Publication.objects.all(), 'Latest reads')

@login_required
def create(request):
    """
        Creates a new publication and marks the user as having read it.
    """
    form = PublicationForm(request.POST or None)

    if form.is_valid():
        publication = form.save(commit=False)
        publication.owner = request.user
        publication.save()

        reading = Reading(user=request.user, publication=publication, rating=form.cleaned_data.get('rating', '1'))
        reading.save()

        request.user.message_set.create(message='You have created and read %s' % publication.title)

        return HttpResponseRedirect(request.POST.get('next', reverse('pub_latest')))

    return render_to_response('publications/create.html',
        {'form': form},
        context_instance=RequestContext(request)
    )

@login_required
def read(request, publication_id):
    """
        Marks the current user as having read the publication.
    """
    form = ReadingForm(request.POST or None)

    # ensure publication exists
    try:
        publication = Publication.objects.get(id=publication_id)
    except Publication.DoesNotExist:
        raise Http404

    # ensure user has not already read this publication
    try:
        reading = Reading.objects.get(publication=publication, user=request.user)
    except Reading.DoesNotExist:
        pass # expected
    else:
        raise Http404

    if form.is_valid():
        reading = form.save(commit=False)
        reading.user = request.user
        reading.publication = publication
        reading.save()
        request.user.message_set.create(message='You have read %s' % (publication.title))

        return HttpResponseRedirect(request.POST.get('next', reverse('pub_latest')))

    return render_to_response('publications/view.html',
        {'publication': publication, 'reading_form': form},
        context_instance=RequestContext(request)
    )

def view(request, publication_id):
    """
        Displays the publication along with a reading if it exista and the first 5 existing quotes.
    """
    form = ReadingForm()
    quote_form = QuoteForm()
    reading = None

    # ensure publication exists
    try:
        publication = Publication.objects.get(id=publication_id)
    except Publication.DoesNotExist:
        raise Http404

    # get reading
    try:
        if not request.user.is_authenticated():
            raise Reading.DoesNotExist
        reading = Reading.objects.get(publication=publication, user=request.user)
    except Reading.DoesNotExist:
        pass
    
    # get quotes
    quotes = publication.quote_set.all()[:5]

    return render_to_response('publications/view.html',
        {
            'publication': publication,
            'reading': reading,
            'reading_form': form,
            'quote_form': quote_form,
            'quotes': quotes
        },
        context_instance=RequestContext(request)
    )

def reads(request, username):
    """
       Displays publications the user has read. Uses pagination.
    """

    #ensure user exists
    try:
        user = User.objects.get(username=username) 
    except User.DoesNotExist:
        raise Http404

    return get_reads(request, user.reader_publication_set.all(), 'Your reads')

def get_reads(request, publication_list, header):
    """
        Returns reads (either latest or a user's reads).
    """

    readings = []

    # setup pagination
    paginator = Paginator(publication_list, 5)

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
    context = {'publications': publications, 'reading_form': reading_form, 'header': header}

    return render_to_response('publications/latest.html',
        context,
        context_instance=RequestContext(request)
    )

@login_required
def quote(request, publication_id):
    """
        Adds a quote to the publication.
    """
    form = QuoteForm(request.POST or None)

    # ensure publication exists
    try:
        publication = Publication.objects.get(id=publication_id)
    except Publication.DoesNotExist:
        raise Http404

    if form.is_valid():
        quote = form.save(commit=False)
        quote.publication = publication
        quote.save()
        request.user.message_set.create(message='You have added a quote to %s' % (publication.title))

        return HttpResponseRedirect(request.POST.get('next', reverse('pub_latest')))

    # get first 5 quotes
    quotes = publication.quote_set.all()[:5]

    return render_to_response('publications/view.html',
        {
            'publication': publication,
            'quote_form': form,
            'quotes': quotes
        },
        context_instance=RequestContext(request)
    )

