from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def adm_required(view_func):
    @login_required(login_url='/usuario/login/')
    def proibido(request, *args, **kwargs):
        if not getattr(request.user, 'adm', False):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return proibido
