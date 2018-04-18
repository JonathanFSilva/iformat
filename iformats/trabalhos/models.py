from django.db import models
from django.contrib.auth.models import User

from django.core import validators

import re

class Grau(models.Model):
    grau = models.CharField('Titulo', max_length=50)
    sigla = models.CharField('Sigla', max_length=10)

    def __str__(self):
        return self.grau


class Curso(models.Model):
    nome_curso = models.CharField('Nome do curso', max_length=100)
    titulacao_curso = models.ForeignKey(Grau, verbose_name='Titulo do curso', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nome_curso


class Trabalho(models.Model):
    usuario = models.ForeignKey(User, verbose_name='Usuario', on_delete=models.CASCADE)

    # Informações da instituição
    instituicao = models.CharField('Nome da instituição', max_length=100, default='Instituto Federal de Educação, Ciência e Tecnologia do Sul de Minas Gerais')
    abreviatura = models.CharField('Abreviatura', max_length=50, default='IFSULDEMINAS')
    departamento = models.CharField('Campus', max_length=50, default='Campus Muzambinho')
    local = models.CharField('Local do campus', max_length=50, default='Muzambinho')

    # Informações do trabalho
    nome_autor = models.CharField('Nome do autor', max_length=50)
    sobrenome_autor = models.CharField('Sobrenome do autor', max_length=50)
    titulo = models.CharField('Titulo', max_length=150)
    subtitulo = models.CharField('Subtitulo', max_length=100, blank=True)
    programa = models.ForeignKey(Curso, verbose_name='Curso', on_delete=models.SET_NULL, null=True)
    data_apresentacao = models.DateField('Data da apresentação')
    data = models.CharField('Ano', max_length=10)

    # Informações do orientador
    nome_orientador = models.CharField('Nome do orientador', max_length=100)
    titulacao_orientador = models.ForeignKey(Grau, verbose_name='Titulação do orientador', related_name='titulo_orientador', on_delete=models.SET_NULL, null=True)

    # Informações do coorientador
    nome_coorientador = models.CharField('Nome do coorientador', max_length=100, blank=True)
    titulacao_coorientador = models.ForeignKey(Grau, verbose_name='Titulação do coorientador', related_name='titulo_coorientador', on_delete=models.SET_NULL, null=True, blank=True)

    data_criacao = models.DateField(verbose_name='Data de criação', auto_now_add=True)
    ultima_edicao = models.DateTimeField(verbose_name='Ultima edição', blank=True, null=True)

    pdf = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.titulo


# class Referencia(models.Model):
#     pass


class Imagem(models.Model):
    label_imagem = models.CharField('Identificação da imagem', max_length=20)
    legenda_imagem = models.CharField('Legenda da imagem', max_length=50)
    trabalho = models.ForeignKey(Trabalho, verbose_name='Trabalho', on_delete=models.CASCADE)

    def __str__(self):
        return self.label_imagem


class Topico(models.Model):
    titulo_topico = models.CharField('Titulo do topico', max_length=100)
    conteudo_topico = models.TextField('Conteudo', blank=True)
    trabalho = models.ForeignKey(Trabalho, verbose_name='Trabalho', on_delete=models.CASCADE)

    # Atributos para controle
    # indice = models.CharField('Indice do tópico', max_length=10, null=True, blank=True, default=0, validators=[validators.RegexValidator(re.compile('^[1-9]+[\.[1-9]+]*$'), 'O indice deve seguir o padrão x ou x.x!', 'invalid')])
    indice = models.CharField('Indice do tópico', max_length=10, null=True, blank=True, default=0)
    # topico_pai = models.CharField('Topico superior', max_length=10, null=True, blank=True)
    # nivel = models.IntegerField('Nivel do topico', null=True, blank=True)

    def __str__(self):
        return self.titulo_topico

