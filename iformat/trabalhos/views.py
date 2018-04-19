from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.conf import settings

from wsgiref.util import FileWrapper

from . import forms
from . import models
from . import utils

import datetime

import shutil
import os


@login_required
def trabalhos(request):

    trabalhos_list = models.Trabalho.objects.filter(usuario=request.user).order_by('-ultima_edicao')
    paginator = Paginator(trabalhos_list, 5)

    page = request.GET.get('page')

    try:
        trabalhos = paginator.page(page)
    except PageNotAnInteger:
        trabalhos = paginator.page(1)
    except EmptyPage:
        trabalhos = paginator.page(paginator.num_pages)

    data = {
        'trabalhos': trabalhos
    }

    return render(request, 'admin/trabalhos.html', data)


@login_required
def inicio(request, trabalho_id):

    trabalho = get_object_or_404(models.Trabalho, pk=trabalho_id)

    if trabalho.usuario == request.user:

        data = {
            'trabalho': trabalho,
            'menu': utils.monta_menu(trabalho)
        }

        return render(request, 'admin/inicio.html', data)
    else:
        raise Http404('Trabalho não encontrado!')


@login_required
def preambulo(request):

    if request.method == 'POST':
        form = forms.Preambulo_form(request.POST)
        if form.is_valid():
            form.save(request)
            utils.inicializa_trabalho(request, models.Trabalho.objects.filter(usuario=request.user).last())
            trabalho = models.Trabalho.objects.last()

            url = '/trabalhos/{0}/inicio'.format(trabalho.id)

            return redirect(url)
    else:
        form = forms.Preambulo_form()

    cursos = {}
    for grau in models.Grau.objects.all().order_by('grau'):
        cursos[grau] = models.Curso.objects.filter(titulacao_curso=grau).order_by('nome_curso')

    data = {'form': form,
            'cursos': cursos,
    }

    return render(request, 'admin/preambulo/preambulo.html', data)


@login_required
def editar_preambulo(request, trabalho_id):

    trabalho = get_object_or_404(models.Trabalho, pk=trabalho_id)

    if trabalho.usuario == request.user:
        preambulo = models.Trabalho.objects.filter(usuario=request.user).get(pk=trabalho_id)

        if request.method == 'POST':
            form = forms.UpdatePreambulo_form(request.POST, instance=preambulo)
            if form.is_valid():
                form.save(request)
                preambulo.ultima_edicao = datetime.datetime.now()
                preambulo.save()

                messages.add_message(request, messages.SUCCESS, 'Dados alterados com sucesso!')
                return redirect('/trabalhos')
        else:
            form = forms.UpdatePreambulo_form(instance=preambulo)
            messages.add_message(request, messages.ERROR, 'Não foi possível alterar os dados!')

        cursos = {}
        for grau in models.Grau.objects.all().order_by('grau'):
            cursos[grau] = models.Curso.objects.filter(titulacao_curso=grau).order_by('nome_curso')

        data = {
            'form': form,
            'cursos': cursos,
            'menu': utils.monta_menu(trabalho)
        }

        return render(request, 'admin/preambulo/preambulo.html', data)
    else:
        raise Http404('Trabalho não encontrado!')


@login_required
def excluir_trabalho(request, trabalho_id):
    trabalho = get_object_or_404(models.Trabalho, pk=trabalho_id)

    try:
        # os.system('rm -r ' + os.path.join(settings.BASE_DIR, 'media/trabalhos', str(request.user.id), str(trabalho.id)))
        path = os.path.join(settings.BASE_DIR, 'media/trabalhos', str(request.user.id), str(trabalho.id))
        # print(path)
        shutil.rmtree(path)
        # os.removedirs(path)
        trabalho.delete()
        messages.add_message(request, messages.SUCCESS, 'Trabalho excluido com sucesso!')
        return redirect('/trabalhos/')
    except OSError:
        messages.add_message(request, messages.ERROR, 'Não foi possível excluir o trabalho!')
        return redirect('/trabalhos/')


@login_required
def topico(request, trabalho_id):

    trabalho = get_object_or_404(models.Trabalho, pk=trabalho_id)

    if trabalho.usuario == request.user:
        if request.method == 'POST':
            form = forms.Topico_form(request.POST)
            if form.is_valid():
                form.save(models.Trabalho.objects.get(pk=trabalho_id))

                url = '/trabalhos/{0}/inicio'.format(trabalho.id)
                messages.add_message(request, messages.SUCCESS, 'Tópico criado com sucesso!')
                return redirect(url)
        else:
            form = forms.Topico_form()

        data = {'form': form,
                'menu': utils.monta_menu(trabalho)
        }

        return render(request, 'admin/topicos/topicos.html', data)
    else:
        raise Http404('Trabalho não encontrado!')


@login_required
def editar_topico(request, trabalho_id, topico_id):

    trabalho = get_object_or_404(models.Trabalho, pk=trabalho_id)

    if trabalho.usuario == request.user:

        try:
            topico = models.Topico.objects.filter(trabalho_id=trabalho_id).get(id=topico_id)
            if request.method == 'POST':
                form = forms.UpdateTopico_form(request.POST, instance=topico)
                if form.is_valid():
                    form.indice = request.POST['indice' or '0']
                    form.save()
                    trabalho.ultima_edicao = datetime.datetime.now()
                    trabalho.save()

                    messages.add_message(request, messages.SUCCESS, 'Tópico alterado com sucesso!')
                    return redirect('/trabalhos/'+str(trabalho.id)+'/inicio')
            else:
                form = forms.Topico_form(instance=topico)

            data = {'form': form,
                    'menu': utils.monta_menu(trabalho)
            }
            return render(request, 'admin/topicos/topicos.html', data)
        except:
            raise Http404('Tópico não encontrado!')
    else:
        raise Http404('Trabalho não encontrado!')


@login_required
def view_pdf(request, trabalho_id):

    trabalho = get_object_or_404(models.Trabalho, pk=trabalho_id)

    utils.gerar_pdf(request, trabalho)

    with open(trabalho.pdf, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=Trabalho.pdf'
        return response
    pdf.closed


@login_required
def download_pdf(request, trabalho_id):

    trabalho = get_object_or_404(models.Trabalho, pk=trabalho_id)

    if trabalho.usuario == request.user:

        utils.gerar_pdf(request, trabalho)

        try:
            pdf = open(trabalho.pdf, "rb")
            response = HttpResponse(FileWrapper(pdf), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=Trabalho.pdf'
            pdf.close()

            return response
        except:
            raise 'Não foi possivel gerar o pdf!'
    else:
        raise Http404('Trabalho não encontrado!')


# def monta_menu(trabalho):
#
#     data = {
#         'preambulo': models.Trabalho.objects.get(pk=trabalho.id),
#         'pre_textual': models.Topico.objects.filter(trabalho=trabalho).filter(indice=0),
#         'textual': [
#             {obj.titulo_topico: models.Topico.objects.raw("select * from trabalhos_topico where trabalho_id = " + str(trabalho.id) + " and indice like '"+obj.indice+"%';")} for obj in models.Topico.objects.filter(trabalho_id=trabalho.id).filter(topico_pai=None).exclude(indice=0)
#         ],
#         'pos_textual': models.Topico.objects.filter(trabalho=trabalho).filter(indice=6)
#     }
#     # print(data)
#     # return models.Topico.objects.filter(trabalho_id=trabalho.id).order_by('indice')
#     return data
#
#
# def inicializa_trabalho(request, trabalho):
#
#     models.Topico.objects.create(titulo_topico='Dedicatória', trabalho=trabalho, nivel=0, indice=0)
#     models.Topico.objects.create(titulo_topico='Agradecimentos', trabalho=trabalho, nivel=0, indice=0)
#     models.Topico.objects.create(titulo_topico='Epígrafe', trabalho=trabalho, nivel=0, indice=0)
#     models.Topico.objects.create(titulo_topico='Resumo', trabalho=trabalho, nivel=0, indice=0)
#     models.Topico.objects.create(titulo_topico='Abstract', trabalho=trabalho, nivel=0, indice=0)
#     models.Topico.objects.create(titulo_topico='Lista de Abreviaturas', trabalho=trabalho, nivel=0, indice=0)
#
#     models.Topico.objects.create(titulo_topico='Introdução', trabalho=trabalho, nivel=0, indice='1')
#     models.Topico.objects.create(titulo_topico='Contextualização e Motivação', trabalho=trabalho, nivel=1, indice='1.1', topico_pai='1')
#     models.Topico.objects.create(titulo_topico='Justificativa', trabalho=trabalho, nivel=1, indice='1.2', topico_pai='1')
#     models.Topico.objects.create(titulo_topico='Objetivos', trabalho=trabalho, nivel=1, indice='1.3', topico_pai='1')
#     models.Topico.objects.create(titulo_topico='Objetivo Geral', trabalho=trabalho, nivel=2, indice='1.3.1', topico_pai='1.3')
#     models.Topico.objects.create(titulo_topico='Objetivos Específicos', trabalho=trabalho, nivel=2, indice='1.3.2', topico_pai='1.3')
#     models.Topico.objects.create(titulo_topico='Estrutura ou Organização do Trabalho', trabalho=trabalho, nivel=1, indice='1.4', topico_pai='1')
#
#     models.Topico.objects.create(titulo_topico='Revisão de Literatura', trabalho=trabalho, nivel=0, indice='2')
#
#     models.Topico.objects.create(titulo_topico='Metodologia', trabalho=trabalho, nivel=0, indice='3')
#     models.Topico.objects.create(titulo_topico='Tipo de Pesquisa', trabalho=trabalho, nivel=1, indice='3.1', topico_pai='3')
#     models.Topico.objects.create(titulo_topico='Materiais e Métodos', trabalho=trabalho, nivel=1, indice='3.2', topico_pai='3')
#
#     models.Topico.objects.create(titulo_topico='Resultados e Discussão', trabalho=trabalho, nivel=0, indice='4')
#
#     models.Topico.objects.create(titulo_topico='Considerações Finais', trabalho=trabalho, nivel=0, indice='5')
#     models.Topico.objects.create(titulo_topico='Respondendo aos objetivos e contribuições do trabalho', trabalho=trabalho, nivel=1, indice='5.1', topico_pai='5')
#     models.Topico.objects.create(titulo_topico='Proposta de Trabalhos Futuros', trabalho=trabalho, nivel=1, indice='5.2', topico_pai='5')
#
#     try:
#         os.system('mkdir -p ' + os.path.join(settings.BASE_DIR, 'media/trabalhos', str(request.user.id), str(trabalho.id)))
#         os.system('cp ' + os.path.join(settings.BASE_DIR, 'latex/monografia-ifmuz.tar.gz') + ' ' + os.path.join(settings.BASE_DIR, 'media/trabalhos', str(request.user.id), str(trabalho.id)))
#         os.system('tar -vzxf ' + os.path.join(settings.BASE_DIR, 'media/trabalhos', str(request.user.id), str(trabalho.id)) + '/monografia-ifmuz.tar.gz -C ' + os.path.join(settings.BASE_DIR, 'media/trabalhos', str(request.user.id), str(trabalho.id)))
#         os.system('rm ' + os.path.join(settings.BASE_DIR, 'media/trabalhos', str(request.user.id), str(trabalho.id)) + '/monografia-ifmuz.tar.gz')
#
#         trabalho.pdf = '{0}/{1}'.format(os.path.join(settings.BASE_DIR, 'media/trabalhos', str(request.user.id), str(trabalho.id)), 'main.tex')
#         trabalho.save()
#
#     except:
#         raise 'Erro!'
#
#
# def monta_preambulo(request, trabalho_id):
#
#     trabalho = get_object_or_404(models.Trabalho, pk=trabalho_id)
#
#     if trabalho.usuario == request.user:
#         file = open(os.path.join(settings.BASE_DIR, 'media/trabalhos', str(request.user.id), str(trabalho.id), '01-elementos-pre-textuais/preambulo.tex'), 'w')
#
#         lines = [
#             '\\instituicao{Instituto Federal de Educação, Ciência e Tecnologia do Sul de Minas Gerais}',
#             '\\abreviatura{IFSULDEMINAS}',
#             '\\departamento{Campus Muzambinho}',
#             '\\local{Muzambinho}',
#             '\\programa{' + trabalho.programa.nome_curso + '}',
#             '\\nomeautor{' + trabalho.nome_autor + '}',
#             '\\sobrenomeautor{' + trabalho.sobrenome_autor + '}',
#             '\\titulotb{' + trabalho.titulo + '}',
#             '\\subtitulo{' + trabalho.subtitulo + '}',
#             '\\data{' + trabalho.data + '}',
#             '\\grau{' + trabalho.programa.titulacao_curso.grau + '}',
#             '\\dataapresentacao{' + trabalho.data_apresentacao.__format__('%d-%m-%Y') + '}',
#             '\\orientador{' + trabalho.nome_orientador + '}',
#             '\\titulacaoorientador{' + trabalho.titulacao_orientador.sigla + '}',
#         ]
#
#         if trabalho.nome_coorientador:
#             lines.append('\\coorientador{' + trabalho.nome_coorientador + '}')
#
#         if trabalho.titulacao_coorientador:
#             lines.append('\\titulacaocoorientador{' + trabalho.titulacao_coorientador.sigla + '}')
#
#         for line in lines:
#             file.write(line)
#             file.write('\n')
#
#         file.close()
#
#     else:
#         raise Http404('Trabalho não encontrado!')
#
#
# def monta_pre_textual(request, trabalho_id):
#
#     trabalho = get_object_or_404(models.Trabalho, pk=trabalho_id)
#
#     if trabalho.usuario == request.user:
#         try:
#             os.chdir(os.path.join(settings.BASE_DIR, 'media/trabalhos', str(request.user.id), str(trabalho.id)))
#             # os.system('latex main.tex')
#             os.system('pdflatex main.tex')
#
#             return redirect('/trabalhos')
#         except:
#             raise 'Não foi possivel gerar o pdf!'
#     else:
#         raise Http404('Trabalho não encontrado!')
#
#
# def monta_textual(request, trabalho_id):
#
#     trabalho = get_object_or_404(models.Trabalho, pk=trabalho_id)
#
#     if trabalho.usuario == request.user:
#         try:
#             os.chdir(os.path.join(settings.BASE_DIR, 'media/trabalhos', str(request.user.id), str(trabalho.id)))
#             # os.system('latex main.tex')
#             os.system('pdflatex main.tex')
#
#             return redirect('/trabalhos')
#         except:
#             raise 'Não foi possivel gerar o pdf!'
#     else:
#         raise Http404('Trabalho não encontrado!')
#
#
# def monta_pos_textual(request, trabalho_id):
#
#     trabalho = get_object_or_404(models.Trabalho, pk=trabalho_id)
#
#     if trabalho.usuario == request.user:
#         try:
#             os.chdir(os.path.join(settings.BASE_DIR, 'media/trabalhos', str(request.user.id), str(trabalho.id)))
#             # os.system('latex main.tex')
#             os.system('pdflatex main.tex')
#
#             return redirect('/trabalhos')
#         except:
#             raise 'Não foi possivel gerar o pdf!'
#     else:
#         raise Http404('Trabalho não encontrado!')
