from django.shortcuts import render
from django import forms
import os
import random

from . import util
import markdown2

class MainForm(forms.Form):
    name = forms.CharField(label=False, max_length=100, required=True)
    body = forms.CharField(required=True, label=False, widget=forms.Textarea(attrs={
        'class': 'form-control main-text-box',
        'id': 'main_text'
    }))

class EditForm(forms.Form):
    body = forms.CharField(required=True, label=False, widget=forms.Textarea(attrs={
        'class': 'form-control main-text-box',
        'id': 'main_text'
    }))

class SearchForm(forms.Form):
    name = forms.CharField(label=False, max_length=100, widget=forms.TextInput(attrs={
        "class": "search"
    }))


def index(request):

    if request.method == 'GET':
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "SearchForm": SearchForm
        })
    

def entry(request, name):

    if util.get_entry(name) != None:
        entry = markdown2.markdown(util.get_entry(name))
        request.session['name'] = name

        return render(request, "encyclopedia/entries.html", {
            'entry': entry,
            "SearchForm": SearchForm
        })
    else:
        return render(request, "encyclopedia/not_found.html")   


def new_page(request):

    form = MainForm

    if request.method == 'GET':
        return render(request, "encyclopedia/new_page.html", {
            'form': form,
            "SearchForm": SearchForm
        })

    if request.method == 'POST':
        form = MainForm(request.POST)
        if form.is_valid():

            name = form.cleaned_data['name']
            body = form.cleaned_data['body']

            if util.get_entry(name) == None:

                md_content = '# ' + name + '\n\n' + body

                with open(os.path.join('entries' ,name + '.md'), 'w', encoding='ISO-8859-15') as f:
                    f.write(md_content)
                
                name = name
                entry = markdown2.markdown(util.get_entry(name))
                request.session['name'] = name

                return render(request, "encyclopedia/entries.html", {
                    'entry': entry,
                    "SearchForm": SearchForm
                })

            else:
                error = 'The entry you are trying to create already exists.'
                return render(request, "encyclopedia/new_page.html", {
                    'form': form,
                    'error': error,
                    "SearchForm": SearchForm
                })   


def search(request):

    form = SearchForm

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():

            name = form.cleaned_data['name']

            if util.get_entry(name) != None:
                entry = markdown2.markdown(util.get_entry(name))
                request.session['name'] = name

                return render(request, "encyclopedia/entries.html", {
                    'entry': entry,
                    "SearchForm": SearchForm
                })
            else:
                entries = util.list_entries()
                sub_entries = []
                for entry in entries:
                    if str(name).upper() in entry.upper():
                        sub_entries.append(entry)
                if sub_entries:
                    return render(request, "encyclopedia/index.html", {
                        "name": 'Similar results',
                        "entries": sub_entries,
                        "SearchForm": SearchForm
                    })
                else:    
                    return render(request, "encyclopedia/not_found.html", {
                        "SearchForm": SearchForm
                    })


def random_page(request):

    if request.method == 'GET':
        names = util.list_entries()
        name = random.choice(names)
        request.session['name'] = name
        entry = markdown2.markdown(util.get_entry(name))
        return render(request, "encyclopedia/entries.html", {
                        'entry': entry,
                        "SearchForm": SearchForm
                })


def edit_page(request):

    if request.method == 'GET':
        name = request.session['name']
        entry = util.get_entry(name)
        return render(request, "encyclopedia/edit_page.html", {
                        'name': name,
                        'entry': entry,
                        'form': EditForm({'body': entry}),
                        "SearchForm": SearchForm
                    })

    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():

            md_content = form.cleaned_data['body']
            name = request.session['name']

            with open(os.path.join('entries' ,name + '.md'), 'w', encoding='ISO-8859-15') as f:
                print(md_content)
                f.write(md_content)

            entry = markdown2.markdown(util.get_entry(name))
            request.session['name'] = name

            return render(request, "encyclopedia/entries.html", {
                'entry': entry,
                "SearchForm": SearchForm
            })