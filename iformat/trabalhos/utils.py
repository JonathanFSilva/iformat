from django.shortcuts import redirect, get_object_or_404
from django.conf import settings
from django.http import Http404

from . import models

import shutil
import os


def monta_menu(trabalho):
    data = {
        'preambulo': models.Trabalho.objects.get(pk=trabalho.id),
        'pre_textual': models.Topico.objects.filter(trabalho=trabalho).filter(indice=0),
        'textual': [
            {obj.titulo_topico: models.Topico.objects.filter(trabalho=trabalho).filter(indice__startswith=obj.indice)}
            for obj in models.Topico.objects.filter(trabalho=trabalho).exclude(indice=0).exclude(indice__contains='.')
        ],
        'pos_textual': models.Topico.objects.filter(trabalho=trabalho).filter(indice=6)
    }

    return data


def inicializa_trabalho(request, trabalho):
    models.Topico.objects.create(titulo_topico='Dedicatória', trabalho=trabalho, indice=0)
    models.Topico.objects.create(titulo_topico='Agradecimentos', trabalho=trabalho, indice=0)
    models.Topico.objects.create(titulo_topico='Epígrafe', trabalho=trabalho, indice=0)
    models.Topico.objects.create(titulo_topico='Resumo', trabalho=trabalho, indice=0)
    models.Topico.objects.create(titulo_topico='Abstract', trabalho=trabalho, indice=0)
    models.Topico.objects.create(titulo_topico='Lista de Abreviaturas', trabalho=trabalho, indice=0)

    models.Topico.objects.create(titulo_topico='Introdução', trabalho=trabalho, indice='1')
    models.Topico.objects.create(titulo_topico='Contextualização e Motivação', trabalho=trabalho, indice='1.1')
    models.Topico.objects.create(titulo_topico='Justificativa', trabalho=trabalho, indice='1.2')
    models.Topico.objects.create(titulo_topico='Objetivos', trabalho=trabalho, indice='1.3')
    models.Topico.objects.create(titulo_topico='Objetivo Geral', trabalho=trabalho, indice='1.3.1')
    models.Topico.objects.create(titulo_topico='Objetivos Específicos', trabalho=trabalho, indice='1.3.2')
    models.Topico.objects.create(titulo_topico='Estrutura ou Organização do Trabalho', trabalho=trabalho, indice='1.4')

    models.Topico.objects.create(titulo_topico='Revisão de Literatura', trabalho=trabalho, indice='2')

    models.Topico.objects.create(titulo_topico='Metodologia', trabalho=trabalho, indice='3')
    models.Topico.objects.create(titulo_topico='Tipo de Pesquisa', trabalho=trabalho, indice='3.1')
    models.Topico.objects.create(titulo_topico='Materiais e Métodos', trabalho=trabalho, indice='3.2')

    models.Topico.objects.create(titulo_topico='Resultados e Discussão', trabalho=trabalho, indice='4')

    models.Topico.objects.create(titulo_topico='Considerações Finais', trabalho=trabalho, indice='5')
    models.Topico.objects.create(titulo_topico='Respondendo aos objetivos e contribuições do trabalho', trabalho=trabalho, indice='5.1')
    models.Topico.objects.create(titulo_topico='Proposta de Trabalhos Futuros', trabalho=trabalho, indice='5.2')

    try:
        path = os.path.join(settings.BASE_DIR, 'media/trabalhos', str(request.user.id), str(trabalho.id))

        os.makedirs(path)
        os.chdir(path)

        os.system('cp ' + os.path.join(settings.BASE_DIR, 'latex/monografia-ifmuz.tar.gz .'))
        os.system('tar -vzxf monografia-ifmuz.tar.gz')

        os.remove('monografia-ifmuz.tar.gz')

        trabalho.pdf = '{0}/{1}'.format(path, 'main.pdf')

        trabalho.save()

    except:
        raise 'Erro ao inicializar o projeto!'


def gera_tex(request, topico):

    temp = os.path.join(settings.BASE_DIR, 'media/trabalhos', str(request.user.id), str(topico.trabalho_id), 'temp')

    file = open(os.path.join(temp, topico.indice + '.html'), 'w', encoding='utf-8')
    file.writelines(topico.conteudo_topico)
    file.close()

    os.system('pandoc ' + os.path.join(temp, topico.indice + '.html') + ' -o ' + os.path.join(temp, topico.indice + '.tex'))

    file = open(os.path.join(temp, topico.indice + '.tex'), 'r', encoding='utf-8')
    content = file.readlines()
    file.close()

    return content


def monta_preambulo(request, trabalho_id):

    trabalho = get_object_or_404(models.Trabalho, pk=trabalho_id)

    path = os.path.join(settings.BASE_DIR, 'media/trabalhos', str(request.user.id), str(trabalho.id))

    if trabalho.usuario == request.user:
        file = open(os.path.join(path, '01-elementos-pre-textuais/preambulo.tex'), 'w', encoding="utf-8")

        lines = [
            '\\instituicao{Instituto Federal de Educação, Ciência e Tecnologia do Sul de Minas Gerais}',
            '\\abreviatura{IFSULDEMINAS}',
            '\\departamento{Campus Muzambinho}',
            '\\local{Muzambinho}',
            '\\programa{' + trabalho.programa.nome_curso + '}',
            '\\nomeautor{' + trabalho.nome_autor + '}',
            '\\sobrenomeautor{' + trabalho.sobrenome_autor + '}',
            '\\titulotb{' + trabalho.titulo + '}',
            '\\subtitulo{' + trabalho.subtitulo + '}',
            '\\data{' + trabalho.data + '}',
            '\\grau{' + trabalho.programa.titulacao_curso.grau + '}',
            '\\dataapresentacao{' + trabalho.data_apresentacao.__format__('%d-%m-%Y') + '}',
            '\\orientador{' + trabalho.nome_orientador + '}',
            '\\titulacaoorientador{' + trabalho.titulacao_orientador.sigla + '}',
        ]

        if trabalho.nome_coorientador:
            lines.append('\\coorientador{' + trabalho.nome_coorientador + '}')

        if trabalho.titulacao_coorientador:
            lines.append('\\titulacaocoorientador{' + trabalho.titulacao_coorientador.sigla + '}')

        for line in lines:
            file.write(line)
            file.write('\n')

        file.close()

    else:
        raise Http404('Trabalho não encontrado!')


def monta_agradecimentos(request, trabalho_id):
    trabalho = get_object_or_404(models.Trabalho, pk=trabalho_id)

    path = os.path.join(settings.BASE_DIR, 'media/trabalhos', str(request.user.id), str(trabalho.id))

    if trabalho.usuario == request.user:
        file = open(os.path.join(path, '01-elementos-pre-textuais/agradecimentos.tex'), 'w', encoding="utf-8")

        agradecimentos = models.Topico.objects.filter(trabalho=trabalho).get(titulo_topico='Agradecimentos')

        lines = [
            '\\begin{agradecimento}',
            # str(agradecimentos.conteudo_topico),
            # '\\end{agradecimento}'
        ]

        conteudo = gera_tex(request, agradecimentos)
        for c in conteudo:
            lines.append(str(c))

        lines.append('\\end{agradecimento}')

        for line in lines:
            file.write(line)
            file.write('\n')

        file.close()
    else:
        raise Http404('Trabalho não encontrado!')


def monta_dedicatoria(request, trabalho_id):
    trabalho = get_object_or_404(models.Trabalho, pk=trabalho_id)

    path = os.path.join(settings.BASE_DIR, 'media/trabalhos', str(request.user.id), str(trabalho.id))

    if trabalho.usuario == request.user:
        file = open(os.path.join(path, '01-elementos-pre-textuais/dedicatoria.tex'), 'w', encoding="utf-8")

        dedicatoria = models.Topico.objects.filter(trabalho=trabalho).get(titulo_topico='Dedicatória')

        lines = [
            '\\begin{dedicatoria}',
            '\\begin{flushright}',
            '\\textbf{DEDICATÓRIA}',
            '\\end{flushright}',
            # str(dedicatoria.conteudo_topico),
            # '\\end{dedicatoria}'
        ]

        conteudo = gera_tex(request, dedicatoria)
        for c in conteudo:
            lines.append(str(c))

        lines.append('\\end{dedicatoria}')

        for line in lines:
            file.write(line)
            file.write('\n')

        file.close()
    else:
        raise Http404('Trabalho não encontrado!')


# def monta_epigrafe(request, trabalho_id):
#     trabalho = get_object_or_404(models.Trabalho, pk=trabalho_id)
#
#     if trabalho.usuario == request.user:
#         file = open(os.path.join(os.path.join(settings.BASE_DIR, 'media/trabalhos', str(request.user.id), str(trabalho.id), '01-elementos-pre-textuais/epigrafe.tex')), 'w')
#
#         dedicatoria = models.Topico.objects.filter(trabalho=trabalho).get(titulo_topico='Dedicatória')
#
#         if dedicatoria.conteudo_topico:
#
#             lines = [
#                 '\\begin{epigrafe}',
#                 '\\begin{flushright}',
#                 '\\textbf{DEDICATÓRIA}',
#                 '\\end{flushright}',
#                 str(dedicatoria.conteudo_topico),
#                 '\\end{epigrafe}'
#             ]
#
#             for line in lines:
#                 file.write(line)
#                 file.write('\n')
#
#             file.close()
#     else:
#         raise Http404('Trabalho não encontrado!')


def monta_resumo(request, trabalho_id):
    trabalho = get_object_or_404(models.Trabalho, pk=trabalho_id)

    path = os.path.join(settings.BASE_DIR, 'media/trabalhos', str(request.user.id), str(trabalho.id))

    if trabalho.usuario == request.user:
        file = open(os.path.join(path, '01-elementos-pre-textuais/resumoPt.tex'), 'w', encoding="utf-8")

        paginas = None
        try:
            os.chdir(os.path.join(settings.BASE_DIR, 'media/trabalhos', str(request.user.id), str(trabalho.id)))
            os.system("pdfinfo main.pdf | grep Pages | awk '{s+=$2}END{print s}'")
        except:
            raise "Erro ao contar as páginas!"

        resumo = models.Topico.objects.filter(trabalho=trabalho).get(titulo_topico='Resumo')

        lines = [
            '\\begin{RESUMO}\n',
            '\\thispagestyle{empty}\n',
            '\\begin{SingleSpace}\n',
            '\\noindent\n',
            '{\\imprimirsobrenomeautor}, {\\imprimirnomeautor}. \\textbf{{\\imprimirtitulotb}}. '
            '{\\imprimirdata}. ' + str(paginas) + '. Trabalho de Conclusão de Curso (Curso de {\\imprimirprograma}) – {\\imprimirinstituicao} – {\\imprimirdepartamento}, {\\imprimirlocal}, {\\imprimirdata}.\n'
            '\\end{SingleSpace}\n',
            '\\vspace{1cm}\n',
            '\\begin{center}\n',
            '\\textbf{RESUMO}\n',
            '\\end{center}\n',
            '\\begin{SingleSpace}\n',
            # '\\hspace{-1.3 cm}' + ''
            # str(resumo.conteudo_topico) + '\n',
            # '\\end{SingleSpace}\n',
            # '\\end{RESUMO}\n'
        ]

        conteudo = gera_tex(request, resumo)
        for c in conteudo:
            lines.append(str(c))

        lines.append('\\end{SingleSpace}\n')
        lines.append('\\end{RESUMO}\n')

        for line in lines:
            file.write(line)
            # file.write('\n')

        file.close()
    else:
        raise Http404('Trabalho não encontrado!')


def monta_abstract(request, trabalho_id):
    trabalho = get_object_or_404(models.Trabalho, pk=trabalho_id)

    path = os.path.join(settings.BASE_DIR, 'media/trabalhos', str(request.user.id), str(trabalho.id))

    if trabalho.usuario == request.user:
        file = open(os.path.join(path, '01-elementos-pre-textuais/resumoEn.tex'), 'w', encoding="utf-8")

        resumo = models.Topico.objects.filter(trabalho=trabalho).get(titulo_topico='Abstract')

        lines = [
            '\\begin{ABSTRACT}\n',
            # '\\thispagestyle{empty}\n',
            '\\begin{SingleSpace}\n',
            '\\noindent\n',
            '{\\imprimirsobrenomeautor}, {\\imprimirnomeautor}. \\textbf{{\\imprimirtitulotb}}. '
            '{\\imprimirdata}. nf. Trabalho de Conclusão de Curso (Curso de {\\imprimirprograma}) – {\\imprimirinstituicao} – {\\imprimirdepartamento}, {\\imprimirlocal}, {\\imprimirdata}.\n'
            '\\end{SingleSpace}\n',
            '\\vspace{1cm}\n',
            '\\begin{center}\n',
            '\\textbf{ABSTRACT}\n',
            '\\end{center}\n',
            '\\begin{SingleSpace}\n',
            # '\\hspace{-1.3 cm}' +
            # str(resumo.conteudo_topico) + '\n',
            # '\\end{SingleSpace}\n',
            # '\\end{ABSTRACT}\n'
        ]

        conteudo = gera_tex(request, resumo)
        for c in conteudo:
            lines.append(str(c))

        lines.append('\\end{SingleSpace}\n')
        lines.append('\\end{ABSTRACT}\n')

        for line in lines:
            file.write(line)
            # file.write('\n')

        file.close()
    else:
        raise Http404('Trabalho não encontrado!')


def monta_introducao(request, trabalho_id):
    trabalho = get_object_or_404(models.Trabalho, pk=trabalho_id)

    path = os.path.join(settings.BASE_DIR, 'media/trabalhos', str(request.user.id), str(trabalho.id))

    if trabalho.usuario == request.user:
        file = open(os.path.join(path, '02-elementos-textuais/1-introducao.tex'), 'w', encoding="utf-8")

        # topicos = models.Topico.objects.raw("select * from trabalhos_topico where trabalho_id = " + str(trabalho.id) + " and indice LIKE '1%';")
        topicos = models.Topico.objects.filter(trabalho=trabalho).filter(indice__startswith='1')

        for topico in topicos:
            # print(topico.indice)
            sec = str(topico.indice).split('.')

            if len(sec) == 1:
                lines = [
                    '\\chapter{' + str(topico.titulo_topico) + '}\n',
                    # str(topico.conteudo_topico) + '\n',
                    # str(conteudo) + '\n',
                ]
            elif len(sec) == 2:
                lines = [
                    '\\section{' + str(topico.titulo_topico) + '}\n',
                    # str(topico.conteudo_topico) + '\n',
                    # str(conteudo) + '\n',
                ]
            elif len(sec) == 3:
                lines = [
                    '\\subsection{' + str(topico.titulo_topico) + '}\n',
                    # str(topico.conteudo_topico) + '\n',
                    # str(conteudo) + '\n',
                ]
            elif len(sec) == 4:
                lines = [
                    '\\subsubsection{' + str(topico.titulo_topico) + '}\n',
                    # str(topico.conteudo_topico) + '\n',
                    # str(conteudo) + '\n',
                ]
            elif len(sec) == 5:
                lines = [
                    '\\subsubsubsection{' + str(topico.titulo_topico) + '}\n',
                    # str(topico.conteudo_topico) + '\n',
                    # str(conteudo) + '\n',
                ]

            conteudo = gera_tex(request, topico)
            for c in conteudo:
                lines.append(str(c))

            for line in lines:
                file.write(line)

        file.close()

    else:
        raise Http404('Trabalho não encontrado!')


def monta_revisao_literatura(request, trabalho_id):
    trabalho = get_object_or_404(models.Trabalho, pk=trabalho_id)

    path = os.path.join(settings.BASE_DIR, 'media/trabalhos', str(request.user.id), str(trabalho.id))

    if trabalho.usuario == request.user:
        file = open(os.path.join(path, '02-elementos-textuais/2-revisao_de_literatura.tex'), 'w', encoding="utf-8")

        # topicos = models.Topico.objects.raw("select * from trabalhos_topico where trabalho_id = " + str(trabalho.id) + " and indice LIKE '2%';")
        topicos = models.Topico.objects.filter(trabalho=trabalho).filter(indice__startswith=2)

        for topico in topicos:

            sec = str(topico.indice).split('.')

            if len(sec) == 1:
                lines = [
                    '\\chapter{' + str(topico.titulo_topico) + '}\n',
                    # str(topico.conteudo_topico) + '\n',
                ]
            elif len(sec) == 2:
                lines = [
                    '\\section{' + str(topico.titulo_topico) + '}\n',
                    # str(topico.conteudo_topico) + '\n',
                ]
            elif len(sec) == 3:
                lines = [
                    '\\subsection{' + str(topico.titulo_topico) + '}\n',
                    # str(topico.conteudo_topico) + '\n',
                ]
            elif len(sec) == 4:
                lines = [
                    '\\subsubsection{' + str(topico.titulo_topico) + '}\n',
                    # str(topico.conteudo_topico) + '\n',
                ]
            elif len(sec) == 5:
                lines = [
                    '\\subsubsubsection{' + str(topico.titulo_topico) + '}\n',
                    # str(topico.conteudo_topico) + '\n',
                ]

            conteudo = gera_tex(request, topico)
            for c in conteudo:
                lines.append(str(c))

            for line in lines:
                file.write(line)
                # file.write('\n')
        file.close()

    else:
        raise Http404('Trabalho não encontrado!')


def monta_metodologia(request, trabalho_id):
    trabalho = get_object_or_404(models.Trabalho, pk=trabalho_id)

    path = os.path.join(settings.BASE_DIR, 'media/trabalhos', str(request.user.id), str(trabalho.id))

    if trabalho.usuario == request.user:
        file = open(os.path.join(path, '02-elementos-textuais/3-metodologia.tex'), 'w', encoding="utf-8")

        # topicos = models.Topico.objects.raw("select * from trabalhos_topico where trabalho_id = " + str(trabalho.id) + " and indice LIKE '3%';")
        topicos = models.Topico.objects.filter(trabalho=trabalho).filter(indice__startswith=3)

        for topico in topicos:

            sec = str(topico.indice).split('.')

            if len(sec) == 1:
                lines = [
                    '\\chapter{' + str(topico.titulo_topico) + '}\n',
                    # str(topico.conteudo_topico) + '\n',
                ]
            elif len(sec) == 2:
                lines = [
                    '\\section{' + str(topico.titulo_topico) + '}\n',
                    # str(topico.conteudo_topico) + '\n',
                ]
            elif len(sec) == 3:
                lines = [
                    '\\subsection{' + str(topico.titulo_topico) + '}\n',
                    # str(topico.conteudo_topico) + '\n',
                ]
            elif len(sec) == 4:
                lines = [
                    '\\subsubsection{' + str(topico.titulo_topico) + '}\n',
                    # str(topico.conteudo_topico) + '\n',
                ]
            elif len(sec) == 5:
                lines = [
                    '\\subsubsubsection{' + str(topico.titulo_topico) + '}\n',
                    # str(topico.conteudo_topico) + '\n',
                ]

            conteudo = gera_tex(request, topico)
            for c in conteudo:
                lines.append(str(c))

            for line in lines:
                file.write(line)
                # file.write('\n')
        file.close()

    else:
        raise Http404('Trabalho não encontrado!')


def monta_resultados_discussao(request, trabalho_id):
    trabalho = get_object_or_404(models.Trabalho, pk=trabalho_id)

    path = os.path.join(settings.BASE_DIR, 'media/trabalhos', str(request.user.id), str(trabalho.id))

    if trabalho.usuario == request.user:
        file = open(os.path.join(path, '02-elementos-textuais/4-resultados_e_discussao.tex'), 'w', encoding="utf-8")

        # topicos = models.Topico.objects.raw("select * from trabalhos_topico where trabalho_id = " + str(trabalho.id) + " and indice LIKE '4%';")
        topicos = models.Topico.objects.filter(trabalho=trabalho).filter(indice__startswith=4)

        for topico in topicos:

            sec = str(topico.indice).split('.')

            if len(sec) == 1:
                lines = [
                    '\\chapter{' + str(topico.titulo_topico) + '}\n',
                    # str(topico.conteudo_topico) + '\n',
                ]
            elif len(sec) == 2:
                lines = [
                    '\\section{' + str(topico.titulo_topico) + '}\n',
                    # str(topico.conteudo_topico) + '\n',
                ]
            elif len(sec) == 3:
                lines = [
                    '\\subsection{' + str(topico.titulo_topico) + '}\n',
                    # str(topico.conteudo_topico) + '\n',
                ]
            elif len(sec) == 4:
                lines = [
                    '\\subsubsection{' + str(topico.titulo_topico) + '}\n',
                    # str(topico.conteudo_topico) + '\n',
                ]
            elif len(sec) == 5:
                lines = [
                    '\\subsubsubsection{' + str(topico.titulo_topico) + '}\n',
                    # str(topico.conteudo_topico) + '\n',
                ]

            conteudo = gera_tex(request, topico)
            for c in conteudo:
                lines.append(str(c))

            for line in lines:
                file.write(line)
                # file.write('\n')
        file.close()

    else:
        raise Http404('Trabalho não encontrado!')


def monta_consideracoes_finais(request, trabalho_id):
    trabalho = get_object_or_404(models.Trabalho, pk=trabalho_id)

    path = os.path.join(settings.BASE_DIR, 'media/trabalhos', str(request.user.id), str(trabalho.id))

    if trabalho.usuario == request.user:
        file = open(os.path.join(path, '02-elementos-textuais/5-consideracoes_finais.tex'), 'w', encoding="utf-8")

        # topicos = models.Topico.objects.raw("select * from trabalhos_topico where trabalho_id = " + str(trabalho.id) + " and indice LIKE '5%';")
        topicos = models.Topico.objects.filter(trabalho=trabalho).filter(indice__startswith=5)

        for topico in topicos:

            sec = str(topico.indice).split('.')

            if len(sec) == 1:
                lines = [
                    '\\chapter{' + str(topico.titulo_topico) + '}\n',
                    # str(topico.conteudo_topico) + '\n',
                ]
            elif len(sec) == 2:
                lines = [
                    '\\section{' + str(topico.titulo_topico) + '}\n',
                    # str(topico.conteudo_topico) + '\n',
                ]
            elif len(sec) == 3:
                lines = [
                    '\\subsection{' + str(topico.titulo_topico) + '}\n',
                    # str(topico.conteudo_topico) + '\n',
                ]
            elif len(sec) == 4:
                lines = [
                    '\\subsubsection{' + str(topico.titulo_topico) + '}\n',
                    # str(topico.conteudo_topico) + '\n',
                ]
            elif len(sec) == 5:
                lines = [
                    '\\subsubsubsection{' + str(topico.titulo_topico) + '}\n',
                    # str(topico.conteudo_topico) + '\n',
                ]

            conteudo = gera_tex(request, topico)
            for c in conteudo:
                lines.append(str(c))

            for line in lines:
                file.write(line)
                # file.write('\n')
        file.close()

    else:
        raise Http404('Trabalho não encontrado!')


# def monta_pos_textual(request, trabalho_id):
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


def gerar_pdf(request, trabalho):
    path = os.path.join(settings.BASE_DIR, 'media/trabalhos', str(request.user.id), str(trabalho.id))

    try:
        temp = os.path.join(path, 'temp')
        os.makedirs(temp)
    except:
        pass

    try:
        monta_preambulo(request, trabalho.id)

        monta_dedicatoria(request, trabalho.id)
        monta_agradecimentos(request, trabalho.id)
        # monta_epigrafe(request, trabalho.id)
        monta_resumo(request, trabalho.id)
        monta_abstract(request, trabalho.id)

        monta_introducao(request, trabalho.id)
        monta_revisao_literatura(request, trabalho.id)
        monta_metodologia(request, trabalho.id)
        monta_resultados_discussao(request, trabalho.id)
        monta_consideracoes_finais(request, trabalho.id)

        shutil.rmtree(temp)

        os.chdir(path)
        os.system('latex main.tex')
        os.system('pdflatex main.tex')

        return redirect('/trabalhos')
    except:
        raise 'Não foi possivel gerar o pdf!'
