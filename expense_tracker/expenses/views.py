from django.shortcuts import render, redirect, get_object_or_404
from .forms import ExpenseForm, RegisterForm
from .models import Expense
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import datetime

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'expenses/register.html', {'form': form})

@login_required
def dashboard(request):
    today = datetime.today()
    expenses = Expense.objects.filter(user=request.user, date__month=today.month)
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    category_data = {}
    for cat in Expense.CATEGORY_CHOICES:
        category_data[cat[0]] = expenses.filter(category=cat[0]).aggregate(Sum('amount'))['amount__sum'] or 0

    return render(request, 'expenses/dashboard.html', {'total': total, 'category_data': category_data})

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})

@login_required
def add_expense(request):
    form = ExpenseForm(request.POST or None)
    if form.is_valid():
        expense = form.save(commit=False)
        expense.user = request.user
        expense.save()
        return redirect('expense_list')
    return render(request, 'expenses/expense_form.html', {'form': form})

@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    form = ExpenseForm(request.POST or None, instance=expense)
    if form.is_valid():
        form.save()
        return redirect('expense_list')
    return render(request, 'expenses/expense_form.html', {'form': form})

@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    expense.delete()
    return redirect('expense_list')
