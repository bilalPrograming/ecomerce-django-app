from django.shortcuts import render , get_object_or_404 , redirect
from .models import Item , Category
from django.db.models import Q
from .forms import NewItem , EditItem
from django.contrib.auth.decorators import login_required


def items(request):
    query = request.GET.get('query' , '')
    category_id = request.GET.get('category' , 0)
    items = Item.objects.filter(is_sold = False)
    categories = Category.objects.all()

    if query:
        items = items.filter( Q(name__icontains = query) | Q(description__icontains = query) )

    if category_id:
        items = items.filter( Category_id = category_id)

    return render(request , 'item/items.html' , {
        'items' : items , 
        'query':query ,
        'categories': categories ,
        'category_id': int(category_id)
    })

@login_required
def detail(request , pk):
    item = get_object_or_404(Item , pk = pk)
    releted_items = Item.objects.filter(Category = item.Category, is_sold=False).exclude(pk=pk)[0:3]

    return render(request , 'item/detail.html' , {"item": item , "releted_items" : releted_items})

@login_required
def addItem(request):
    if request.method == "POST":
        form = NewItem(request.POST , request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('item:detail', pk=item.id)
    else:
        form = NewItem()
    return render(request , 'item/itemForm.html' , {'form':form , 'title':'New item'})  

@login_required
def delete(request , pk):
    item = get_object_or_404(Item ,pk = pk , created_by = request.user)
    item.delete()

    return redirect('dashboard:index')

@login_required
def edit(request , pk):
    item = get_object_or_404(Item , pk = pk)
    if request.method == 'POST':
        form = EditItem(request.POST , request.FILES , instance= item)
        if form.is_valid():
            form.save()
            return redirect('item:detail' , pk =item.id)
    else:
        form = EditItem(instance=item)

    return render(request , 'item/edit.html' ,{
        'form' : form , 'title': 'Edit Item'
    })
    
    
