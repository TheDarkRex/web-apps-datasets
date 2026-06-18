from django.contrib import admin
from .models import Dataset, DatasetSchema, Query, Answer


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'size_class', 'owner', 'created_at')
    list_filter = ('size_class', 'created_at')
    search_fields = ('name', 'author', 'description')

@admin.register(DatasetSchema)
class DatasetSchemaAdmin(admin.ModelAdmin):
    list_display = ('dataset',)

@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ('dataset', 'author', 'created_at')
    search_fields = ('content',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('query', 'author', 'created_at')
    search_fields = ('content',)