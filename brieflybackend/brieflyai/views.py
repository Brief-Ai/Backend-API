from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SearchForm
from .models import Search

@login_required
def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            entry = Search(query=query, user=request.user)
            entry.save()
            # Process search results and return the appropriate response
            results = 'a'  # Replace this with your actual search results
            return render(request, 'search_results.html', {'results': results})
    else:
        form = SearchForm()

    return render(request, 'search.html', {'form': form})
