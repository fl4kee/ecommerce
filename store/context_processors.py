from .models import Category


# Context processor
def categories(request):
    return{
        'categories': Category.objects.all(),
    }
