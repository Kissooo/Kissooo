from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Item, Category, BorrowRecord, MaintenanceRecord, Location, StockAdjustment
from .forms import ItemForm, SignUpForm, MaintenanceRecordForm, LocationForm
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
    locations = Location.objects.all()
    selected_category_id = request.GET.get('category')
    selected_location_id = request.GET.get('location')
    query = request.GET.get('q')

    items_list = Item.objects.all().order_by('name')

    if selected_category_id:
        items_list = items_list.filter(category__id=selected_category_id)

    if selected_location_id:
        items_list = items_list.filter(location__id=selected_location_id)

    if query:
        items_list = items_list.filter(
            Q(code__icontains=query) | Q(name__icontains=query)
        )

    paginator = Paginator(items_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'categories': categories,
        'locations': locations,
        'selected_category_id': selected_category_id,
        'selected_location_id': selected_location_id,
    }
    return render(request, 'item_list.html', context)

@login_required
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save()
            if item.quantity > 0:
                StockAdjustment.objects.create(
                    item=item,
                    change=item.quantity,
                    reason="Initial stock",
                    user=request.user
                )
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
    old_quantity = item.quantity

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            updated_item = form.save()
            new_quantity = updated_item.quantity
            change = new_quantity - old_quantity

            if change != 0:
                StockAdjustment.objects.create(
                    item=updated_item,
                    change=change,
                    reason="Manual update",
                    user=request.user
                )
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm(instance=item)
    return render(request, 'item_form.html', {'form': form, 'item': item})

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
    if item.quantity > 0:
        item.quantity -= 1
        item.save()
        StockAdjustment.objects.create(item=item, change=-1, reason="Borrowed", user=request.user)
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

        item = borrow_record.item
        item.quantity += 1
        item.save()
        StockAdjustment.objects.create(item=item, change=1, reason="Returned", user=request.user)
    return redirect('my_borrows')

@login_required
def my_borrows(request):
    borrow_records = BorrowRecord.objects.filter(borrower=request.user).order_by('-borrow_date')
    return render(request, 'my_borrows.html', {'borrow_records': borrow_records})

@login_required
def maintenance_list(request):
    records = MaintenanceRecord.objects.all().order_by('-scheduled_date')
    return render(request, 'maintenance_list.html', {'records': records})

@login_required
def schedule_maintenance(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)
    if request.method == 'POST':
        form = MaintenanceRecordForm(request.POST)
        if form.is_valid():
            maintenance = form.save(commit=False)
            maintenance.item = item
            maintenance.save()
            return redirect('maintenance_list')
    else:
        form = MaintenanceRecordForm()
    return render(request, 'schedule_maintenance.html', {'form': form, 'item': item})

@login_required
def update_maintenance(request, pk):
    record = get_object_or_404(MaintenanceRecord, pk=pk)
    if request.method == 'POST':
        form = MaintenanceRecordForm(request.POST, instance=record)
        if form.is_valid():
            if form.cleaned_data.get('completion_date'):
                record.status = 'COMPLETED'
            form.save()
            return redirect('maintenance_list')
    else:
        form = MaintenanceRecordForm(instance=record)
    return render(request, 'update_maintenance.html', {'form': form, 'record': record})

@login_required
def location_list(request):
    locations = Location.objects.all()
    return render(request, 'location_list.html', {'locations': locations})

@login_required
def location_create(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('location_list')
    else:
        form = LocationForm()
    return render(request, 'location_form.html', {'form': form})

@login_required
def location_update(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return redirect('location_list')
    else:
        form = LocationForm(instance=location)
    return render(request, 'location_form.html', {'form': form})

@login_required
def location_delete(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        location.delete()
        return redirect('location_list')
    return render(request, 'location_confirm_delete.html', {'location': location})
