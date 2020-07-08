from django.contrib import admin
from .models import Project, SubProject


class SubProjectInline(admin.TabularInline):
    model = SubProject
    extra = 0


class ProjectAdmin(admin.ModelAdmin):
    inlines = [SubProjectInline]
    list_display = ('name', 'contractor', 'create_date',
                    'total_receivables', 'total_paid',
                    'num_sub_projects', 'status')
    search_fields = ['name', 'create_date']
    list_per_page = 10


class SubProjectAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_per_page = 10


# admin.site.register(Project, ProjectAdmin)
# admin.site.register(SubProject, SubProjectAdmin)
