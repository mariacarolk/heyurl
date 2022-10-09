from django.shortcuts import render
#CACAU 7 importei HttpResponseNotFound
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from .models import Url
from .models import Click
#cacau
from .forms import OriginalUrlForm

def index(request):
    urls = Url.objects.order_by('-created_at')

    #context = {'urls': urls}

    #CACAU primeiro preciso instanciar meu objeto do tipo ModelForm
    form = OriginalUrlForm()

    #Envio como contexto
    context = {
        'urls': urls,
        'form': form
    }
    #FIMCACAU
    return render(request, 'heyurl/index.html', context)

def store(request):
    # FIXME: Insert a new URL object into storage

    #ATIVIDADE 1 - Criar o codigo da URL encurtada
    # 1.1 Validar se a URL enviada é válida, se não for, retornar erro
    # - Bonus - verificar se a URL já existe no banco
    # - Criar a URL encurtada
    # - Gravar os dados

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

    # CACAU 6 Validar se a URL enviada é válida, se não for, retornar erro
    # if request.method == "POST":
    #     #Argumento 1 -- name da tag input do form, segundo argumento é o que joga caso não tenha valor
    #     original_url = request.POST.get('original_url', None)
    #FIMCACAU

    #return HttpResponse("Storing a new URL object into storage")

def short_url(request, short_url):
    # FIXME: Do the logging to the db of the click with the user agent and browser

    try:
        object = Url.objects.get(short_url=short_url)

        print(object.original_url)
        object.clicks += 1

        object.save()

        print('object', object.original_url, object.short_url, object.created_at, object.updated_at)
        # url = models.ForeignKey(Url, on_delete=models.CASCADE)
        # browser = models.CharField(max_length=255)
        # platform = models.CharField(max_length=255)
        # created_at = models.DateTimeField('date created')
        # updated_at = models.DateTimeField('date updated')
        click = Click(object,
                      'chrome,'
                      'teste',
                      object.created_at,
                      object.updated_at)
        print('INSTANCIOU', click)
        click.save()

        return HttpResponseRedirect(object.original_url)

    except:
        raise Http404("Sorry this link doesn't exists :(")

    #ATIVIDADE 2 - Buscar no BD o clique na URL gravando o usuário e o browser
    #return HttpResponse("You're looking at url %s" % short_url)

def metrics(request, short_url):
    template = 'heyurl/metrics.html'

    object = Url.objects.get(short_url=short_url)

    context = {
        'mensagem': 'Teste',
        'short_url': short_url
    }

    print('ENTROUUUUU', object.original_url, object.short_url, object.clicks)

    return render(request, template, context)
