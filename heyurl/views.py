from django.shortcuts import render
#CACAU 7 importei HttpResponseNotFound
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from .models import Url, Click
from datetime import date
from django.db.models import Sum
from django.db.models import Count
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from django_user_agents.utils import get_user_agent

#cacau
from .forms import OriginalUrlForm

def index(request):
    urls = Url.objects.order_by('-created_at')

    #CACAU primeiro preciso instanciar meu objeto do tipo ModelForm
    form = OriginalUrlForm()

    #Envio como contexto
    context = {
        'urls': urls,
        'form': form
    }

    return render(request, 'heyurl/index.html', context)

def store(request):
    # FIXME: Insert a new URL object into storage

    template = 'heyurl/store.html'
    context = {}

    form = OriginalUrlForm(request.POST)

    if form.is_valid():
        shortened_object = form.save()

        short_url = request.build_absolute_uri('/') + shortened_object.short_url

        long_url = shortened_object.original_url

        context['short_url'] = short_url
        context['original_url'] = long_url

        return render(request, template, context)

    context['errors'] = form.errors

    return render(request, template, context)

def short_url(request, short_url):
    # FIXME: Do the logging to the db of the click with the user agent and browser

    try:
        object = Url.objects.get(short_url=short_url)

        object.clicks += 1

        object.save()

        #fOREIGN KEY 1 - MANY
        #reverse lookup
        click = object.click_set.create(
            browser = request.user_agent.browser.family,
            platform = request.user_agent.os.family,
            created_at = object.created_at,
            updated_at = object.updated_at
        )

        return HttpResponseRedirect(object.original_url)
    except:
        raise Http404("Sorry this link doesn't exists :(")

def metrics(request, short_url):
    template = 'heyurl/metrics.html'

    #The API automatically follows relationships as far as you need. Use double underscores to separate relationships. This works as many levels deep as you want.
    clicks = (Click.objects.filter(url__short_url=short_url,
                                updated_at__month=date.today().month).values('updated_at__day')).order_by(
        'updated_at__day').annotate(total=Count('updated_at__day'))

    #Different browsers that are used in this month
    browsers = (Click.objects.filter(url__short_url=short_url,
                                     updated_at__month=date.today().month).values('browser')).annotate(
        total=Count('browser'))

    # df = pd.DataFrame(list(browsers))
    # chart = sns.barplot(data=df, x="browser", y="total", palette="pastel")
    #
    # chart.set(title='Different browsers that are used in this month', \
    #           xlabel='Browser', ylabel='Total');
    # plt.savefig('teste.png')

    # Different platforms that are used in this month
    platforms = (Click.objects.filter(url__short_url=short_url,
                                     updated_at__month=date.today().month).values('platform')).annotate(
        total=Count('platform'))

    context = {
        'mensagem': 'Teste',
        'short_url' : short_url,
        'clicks': clicks,
        'browsers': browsers,
        'platforms': platforms,
        'chart' : 'teste.png'
    }

    return render(request, template, context)

def handler404(request, exception):
    print('ENTROU HANDLER')
    return render(request, 'heyurl/404.html')