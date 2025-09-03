from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Item, Category, BorrowRecord
from .forms import ItemForm, SignUpForm
from django.utils import timezone
from django.views.decorators.http import require_POST

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def item_list(request):
    categories = Category.objects.all()
    selected_category_id = request.GET.get('category')
    query = request.GET.get('q')

    items_list = Item.objects.all().order_by('name')

    if selected_category_id:
        items_list = items_list.filter(category__id=selected_category_id)

    if query:
        items_list = items_list.filter(
            Q(code__icontains=query) | Q(name__icontains=query)
        )

    paginator = Paginator(items_list, 5) # Show 5 items per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'categories': categories,
        'selected_category_id': selected_category_id
    }
    return render(request, 'item_list.html', context)

@login_required
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'item_form.html', {'form': form})

@login_required
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'item_detail.html', {'item': item})

@login_required
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'item_form.html', {'form': form})

@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'item_confirm_delete.html', {'item': item})

@login_required
@require_POST
def borrow_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    # Optional: Add logic to check if item quantity > 0
    BorrowRecord.objects.create(item=item, borrower=request.user)
    return redirect('my_borrows')

@login_required
@require_POST
def return_item(request, pk):
    borrow_record = get_object_or_404(BorrowRecord, pk=pk, borrower=request.user)
    if borrow_record.status == 'BORROWED':
        borrow_record.return_date = timezone.now()
        borrow_record.status = 'RETURNED'
        borrow_record.save()
    return redirect('my_borrows')

@login_required
def my_borrows(request):
    borrow_records = BorrowRecord.objects.filter(borrower=request.user).order_by('-borrow_date')
    return render(request, 'my_borrows.html', {'borrow_records': borrow_records})
