from django.views.generic import ListView, DetailView, CreateView,  UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from .models import Dataset, Query, Answer, DatasetSchema
from .forms import DatasetForm, QueryForm, AnswerForm, CustomUserCreationForm, SchemaForm
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.db import transaction


class DatasetListView(ListView):
    model = Dataset
    template_name = 'datasets/dataset_list.html'
    context_object_name = 'datasets'

    def get_queryset(self):
        sort_param = self.request.GET.get('sort', '-created_at')

        if sort_param not in ['name', '-name', '-created_at']:
            sort_param = '-created_at'

        queryset = Dataset.objects.all().order_by(sort_param)

        query = self.request.GET.get('q')
        size_filter = self.request.GET.get('size')

        if query:
            search_conditions = Q(name__icontains=query) | Q(author__icontains=query)

            if self.request.user.is_authenticated:
                advanced_conditions = (
                    Q(description__icontains=query) |
                    Q(queries__content__icontains=query) |
                    Q(queries__answers__content__icontains=query)
                )
                search_conditions = search_conditions | advanced_conditions

            queryset = queryset.filter(search_conditions).distinct()

        if size_filter:
            queryset = queryset.filter(size_class=size_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_query'] = self.request.GET.get('q', '')
        context['current_size'] = self.request.GET.get('size', '')
        context['size_choices'] = Dataset.SizeClass.choices
        return context

class DatasetDetailView(DetailView):
    model = Dataset
    template_name = 'datasets/dataset_detail.html'
    context_object_name = 'dataset'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query_form'] = QueryForm()
        context['answer_form'] = AnswerForm()
        return context

class DatasetCreateView(LoginRequiredMixin, CreateView):
    model = Dataset
    form_class = DatasetForm
    template_name = 'datasets/dataset_form.html'
    success_url = reverse_lazy('datasets:list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DatasetUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Dataset
    form_class = DatasetForm
    template_name = 'datasets/dataset_form.html'

    def test_func(self):
        dataset = self.get_object()
        return dataset.owner == self.request.user

    def get_success_url(self):
        return reverse_lazy('datasets:detail', kwargs={'pk': self.object.pk})

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        Dataset.objects.select_for_update().get(pk=self.kwargs['pk'])

        return super().post(request, *args, **kwargs)


class DatasetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Dataset
    template_name = 'datasets/dataset_confirm_delete.html'
    success_url = reverse_lazy('datasets:list')

    def test_func(self):
        dataset = self.get_object()
        return dataset.owner == self.request.user

class QueryCreateView(LoginRequiredMixin, CreateView):
    model = Query
    form_class = QueryForm

    def form_valid(self, form):
        dataset = get_object_or_404(Dataset, pk=self.kwargs['dataset_pk'])
        form.instance.dataset = dataset
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('datasets:detail', kwargs={'pk': self.kwargs['dataset_pk']})


class AnswerCreateView(LoginRequiredMixin, CreateView):
    model = Answer
    form_class = AnswerForm

    def form_valid(self, form):
        query = get_object_or_404(Query, pk=self.kwargs['query_pk'])
        form.instance.query = query
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('datasets:detail', kwargs={'pk': self.object.query.dataset.pk})

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

class QueryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Query
    template_name = 'datasets/query_confirm_delete.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse_lazy('datasets:detail', kwargs={'pk': self.object.dataset.pk})


class AnswerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Answer
    template_name = 'datasets/answer_confirm_delete.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse_lazy('datasets:detail', kwargs={'pk': self.object.query.dataset.pk})

class SchemaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = DatasetSchema
    form_class = SchemaForm
    template_name = 'datasets/schema_form.html'

    def test_func(self):
        dataset = get_object_or_404(Dataset, pk=self.kwargs['dataset_pk'])
        return dataset.owner == self.request.user

    def get_object(self, queryset=None):
        dataset = get_object_or_404(Dataset, pk=self.kwargs['dataset_pk'])
        schema, created = DatasetSchema.objects.get_or_create(dataset=dataset)
        return schema

    def get_success_url(self):
        return reverse_lazy('datasets:detail', kwargs={'pk': self.kwargs['dataset_pk']})