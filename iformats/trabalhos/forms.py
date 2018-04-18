from django.forms import ModelForm
from django import forms
from . import models

import datetime


class Preambulo_form(ModelForm):

    nome_autor = forms.CharField(label="Nome do autor", widget=forms.TextInput(attrs={'class': 'form-control'}))
    sobrenome_autor = forms.CharField(label="Sobrenome", widget=forms.TextInput(attrs={'class': 'form-control'}))

    # Informações do trabalho
    titulo = forms.CharField(label='Titulo', widget=forms.TextInput(attrs={'class': 'form-control'}))
    subtitulo = forms.CharField(label='Subtitulo', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    programa = forms.ModelChoiceField(queryset=models.Curso.objects.all().order_by('nome_curso'), empty_label='Selecione...', to_field_name='nome_curso', widget=forms.Select(attrs={'class': 'form-control'}))
    data_apresentacao = forms.DateField(label='Data da apresentação', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    # Informações do orientador
    nome_orientador = forms.CharField(label='Nome do orientador', widget=forms.TextInput(attrs={'class': 'form-control'}))
    titulacao_orientador = forms.ModelChoiceField(queryset=models.Grau.objects.all().order_by('grau'), empty_label='Selecione...', to_field_name='grau', widget=forms.Select(attrs={'class': 'form-control'}))

    # Informações do coorientador
    nome_coorientador = forms.CharField(label='Nome do coorientador', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    titulacao_coorientador = forms.ModelChoiceField(queryset=models.Grau.objects.all().order_by('grau'), empty_label='Selecione...', to_field_name='grau', required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    def save(self, request):
        data = self.cleaned_data

        trabalho = models.Trabalho()

        trabalho.usuario = request.user
        trabalho.nome_autor = data['nome_autor']
        trabalho.sobrenome_autor = data['sobrenome_autor']
        trabalho.titulo = data['titulo']
        trabalho.subtitulo = data['subtitulo']
        trabalho.programa = data['programa']
        trabalho.data_apresentacao = data['data_apresentacao']
        trabalho.data = str(trabalho.data_apresentacao).split('-')[0]
        trabalho.nome_orientador = data['nome_orientador']
        trabalho.titulacao_orientador = data['titulacao_orientador']
        trabalho.nome_coorientador = data['nome_coorientador']
        trabalho.titulacao_coorientador = data['titulacao_coorientador']

        trabalho.ultima_edicao = datetime.datetime.now()
        trabalho.save()

    class Meta:
        model = models.Trabalho
        exclude = ['instituicao', 'abreviatura', 'departamento', 'local', 'usuario', 'data', 'pdf']


class UpdatePreambulo_form(ModelForm):
    nome_autor = forms.CharField(label="Nome do autor", widget=forms.TextInput(attrs={'class': 'form-control'}))
    sobrenome_autor = forms.CharField(label="Sobrenome", widget=forms.TextInput(attrs={'class': 'form-control'}))

    # Informações do trabalho
    titulo = forms.CharField(label='Titulo', widget=forms.TextInput(attrs={'class': 'form-control'}))
    subtitulo = forms.CharField(label='Subtitulo', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    programa = forms.ModelChoiceField(queryset=models.Curso.objects.all().order_by('nome_curso'), empty_label='Selecione...', to_field_name='nome_curso', widget=forms.Select(attrs={'class': 'form-control'}))
    data_apresentacao = forms.DateField(label='Data da apresentação', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    # Informações do orientador
    nome_orientador = forms.CharField(label='Nome do orientador', widget=forms.TextInput(attrs={'class': 'form-control'}))
    titulacao_orientador = forms.ModelChoiceField(queryset=models.Grau.objects.all().order_by('grau'), empty_label='Selecione...', to_field_name='grau', widget=forms.Select(attrs={'class': 'form-control'}))

    # Informações do coorientador
    nome_coorientador = forms.CharField(label='Nome do coorientador', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    titulacao_coorientador = forms.ModelChoiceField(queryset=models.Grau.objects.all().order_by('grau'), empty_label='Selecione...', to_field_name='grau', required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = models.Trabalho
        exclude = ['instituicao', 'abreviatura', 'departamento', 'local','usuario', 'data', 'pdf']


class Topico_form(ModelForm):

    indice = forms.CharField(label='Indice', widget=forms.TextInput(attrs={'class': 'form-control'}))
    titulo_topico = forms.CharField(label='Titulo do topico', widget=forms.TextInput(attrs={'class': 'form-control'}))
    conteudo_topico = forms.CharField(label='Conteudo', widget=forms.Textarea(attrs={'class': 'form-control'}))

    def save(self, trabalho):
        data = self.cleaned_data

        topico = models.Topico()

        topico.trabalho = trabalho
        topico.indice = data['indice'] or '0'
        topico.titulo_topico = data['titulo_topico']
        topico.conteudo_topico = data['conteudo_topico']
        topico.topico_pai = topico.indice.split('.')[0]
        trabalho.ultima_edicao = datetime.datetime.now()

        topico.save()

    class Meta:
        model = models.Topico
        exclude = ['trabalho']


class UpdateTopico_form(ModelForm):

    indice = forms.CharField(label='Indice', widget=forms.TextInput(attrs={'class': 'form-control'}))
    titulo_topico = forms.CharField(label='Titulo do topico', widget=forms.TextInput(attrs={'class': 'form-control'}))
    conteudo_topico = forms.CharField(label='Conteudo', widget=forms.Textarea())

    class Meta:
        model = models.Topico
        exclude = ['trabalho']