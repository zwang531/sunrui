from django.shortcuts import render, redirect, get_object_or_404

from .models import Project, SubProject


def index(request):
    if not request.user.is_authenticated:
        return redirect('login:index')
    selected_year = ""
    if request.method == 'POST':
        selected_year = request.POST.get('select-year')
    project_list = Project.objects.order_by('-create_date')
    year_dict = {}
    for project in project_list:
        year_dict[project.create_date.year] = 1
    if selected_year and selected_year != 'all':
        filtered_list = []
        for project in project_list:
            if project.create_date.year == int(selected_year):
                filtered_list.append(project)
        project_list = filtered_list
    summary = {}
    if selected_year and selected_year != 'all' and len(project_list):
        num_projects = len(project_list)
        receivables = 0
        paid = 0
        for project in project_list:
            receivables += project.total_receivables()
            paid += project.total_paid()
        balance = receivables - paid
        if balance < 0:
            balance = 0
        summary = {
            'num_projects': num_projects,
            'receivables': receivables,
            'paid': paid,
            'balance': balance,
        }
    context = {
        'project_list': project_list,
        'year_options': year_dict.keys(),
        'selected_year': selected_year,
        'showSummary': len(summary.keys()) > 0,
        'summary': summary,
        'user': request.user.username,
    }
    return render(request, 'my_app/index.html', context)


def project_detail(request, project_id):
    if not request.user.is_authenticated:
        return redirect('login:index')
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'my_app/project.html', {'project': project, 'user': request.user.username})
