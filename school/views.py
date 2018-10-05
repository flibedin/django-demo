from django.shortcuts import render
from django.views.generic import (
            View, TemplateView, ListView, DetailView,
            CreateView, UpdateView, DeleteView)
from . import models
from django.urls import reverse_lazy


class SchoolListView( ListView ):
    context_object_name = 'schools'
    template_name = 'school_list.html'
    model = models.School

class SchoolCreateView( CreateView ):
    fields = ( 'name', 'principal', 'location')
    model = models.School
    template_name = 'school_form.html'

class SchoolUpdateView( UpdateView ):
    fields = ( 'name', 'principal')
    model = models.School
    template_name = 'school_form.html'

class SchoolDeleteView( DeleteView ):
    model = models.School
    success_url = reverse_lazy('school:list')
    template_name = 'confirm_delete.html'

class SchoolDetailView( DetailView ):
    context_object_name = 'school_detail'
    model = models.School
    template_name = 'school_detail.html'
