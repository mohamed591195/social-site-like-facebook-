from django.http import HttpResponseBadRequest

def is_ajax(f):

    def wrapper(request , *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest
        return f(request, *args, **kwargs)
    
    wrapper.__name__ = f.__name__
    wrapper.__doc__ = f.__doc__
    return wrapper