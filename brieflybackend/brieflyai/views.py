from django.shortcuts import render
from .forms import SearchForm
from .models import Search

def search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        entry = Search(query=query, user=request.user)
        entry.save()
        results = 'a'
        return render(request, 'search_results.html', {'results': results})
    else:
        return render(request, 'search.html', {'form': form})