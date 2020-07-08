from django.contrib.admin import AdminSite


class MyAdminSite(AdminSite):
    site_header = 'Mysite administration'

    def get_app_list(self, request):
        app_list = super(MyAdminSite, self).get_app_list(request)
        ordering = {
            "Groups": 1,
            "Users": 2,
            "Projects": 3,
            "Records": 4,
        }
        for app in app_list:
            app['models'].sort(key=lambda x: ordering[x['name']])
        return app_list


admin_site = MyAdminSite(name='admin')
