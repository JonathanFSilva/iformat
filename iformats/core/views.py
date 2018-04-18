from django.shortcuts import render, redirect, render_to_response
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import RequestContext

from django.contrib import messages

# from iformats.contas.forms import Login_form
from .forms import Contact_form


def index(request):
    # return render(request, 'site/index.html', {'login_form': Login_form, 'form': Contact_form})
    return render(request, 'site/index.html', {'form': Contact_form})


def contact(request):
    form_class = Contact_form

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')
            form_subject = request.POST.get('subject', '')
            form_content = request.POST.get('content', '')

            template = get_template('site/contact_template.txt')
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_subject': form_subject,
                'form_content': form_content,
            }

            content = template.render(context)


            try:
                email = EmailMessage(
                    form_subject,
                    content,
                    contact_email,
                    ['jonathansilva259@gmail.com', 'vimendesilva@gmail.com'],
                    headers={'Reply-To': contact_email}
                )
                email.send()

                resposta = EmailMessage(
                    "Contato IFormat",
                    "Obrigado pela colaboração!",
                    contact_email,
                    [contact_email]
                )
                resposta.send()

                messages.add_message(request, messages.SUCCESS, 'Mensagem enviada com sucesso!')
                return redirect('/#contato')
            except:
                messages.add_message(request, messages.ERROR, 'Não foi possível enviar a menssagem!')
                return redirect('/#contato')

    return redirect('/')


# # HTTP Error 404
# def page_not_found(request):
#     # response = render_to_response('errors/404.html', context_instance=RequestContext(request))
#     # response.status_code = 404
#
#     # return response
#     return render(request, '404.html', status=404)


# @login_required
# def home(request):
#     # return render(request, 'site/index.html', {'login_form': Login_form, 'form': Contact_form})
#     return render(request, 'admin/inicio.html')
