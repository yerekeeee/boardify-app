from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Category, Board, Location, UserProfile
from .forms import BoardForm, UserRegistrationForm, UserProfileForm, UserLoginForm


def home_page(request):
    categories = Category.objects.all()
    latest_boards = Board.objects.filter(is_active_board=True).order_by('-created_at')[:8]
    context = {
        'categories': categories,
        'latest_boards': latest_boards
    }
    return render(request, './client/home.html', context)

def all_boards_page(request):
    board_list = Board.objects.filter(is_active_board=True).order_by('-created_at')
    paginator = Paginator(board_list, 12)
    page_number = request.GET.get('page')
    boards = paginator.get_page(page_number)
    context = {
        'boards': boards,
        'page_number': page_number
    }
    return render(request, './client/all-boards.html', context)

def categories_page(request):
    categories = Category.objects.all()
    locations = Location.objects.all()
    context = {
        'categories': categories,
        'locations': locations
    }
    return render(request, "./client/categories.html", context)

def boards_by_category_page(request, slug):
    category = get_object_or_404(Category, slug=slug)
    board_list = Board.objects.filter(category=category, is_active_board=True).order_by('-created_at')
    paginator = Paginator(board_list, 12)
    page_number = request.GET.get('page')
    boards = paginator.get_page(page_number)
    context = {
        'category': category, 
        'boards': boards
    }
    return render(request, './client/boards-by-category.html', context)

def boards_by_location_page(request, slug):
    location = get_object_or_404(Location, slug=slug)
    board_list = Board.objects.filter(location=location, is_active_board=True).order_by('-created_at')
    paginator = Paginator(board_list, 12)
    page_number = request.GET.get('page')
    boards = paginator.get_page(page_number)
    context = {
        'location': location, 
        'boards': boards
    }
    return render(request, './client/boards-by-location.html', context)

def search_results(request):
    query = request.GET.get('q')
    board_list = Board.objects.filter(title__icontains=query, is_active_board=True)
    paginator = Paginator(board_list, 12)
    page_number = request.GET.get('page')
    boards = paginator.get_page(page_number)
    context = {
        'query': query,
        'boards': boards
    }
    return render(request, './client/search-results.html', context)

def board_detail_page(request, pk):
    board = get_object_or_404(Board, pk=pk)
    author = board.userprofile
    context = {
        'board': board,
        'author': author
    }
    return render(request, './client/board-detail.html', context)

def login_page(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Login successful')
                return redirect('profile_page')
            else:
                messages.error(request, 'Неправильный логин или пароль')
    else:
        form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request, './client/login.html', context)

def sign_up_page(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login_page')
    else:
        form = UserRegistrationForm()
    context = {
        'form': form
    }    
    return render(request, './client/sign-up.html', context)


@login_required
def profile_page(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    context = {
        'profile': profile
    }
    return render(request, './client/profile.html', context)

@login_required
def user_boards_page(request):
    user_profile = UserProfile.objects.get(user=request.user)
    boards = Board.objects.filter(userprofile__user=request.user).order_by('-created_at')
    context = {
        'boards': boards
    }
    return render(request, './client/user-boards.html', context)

@login_required
def create_board_page(request):
    if request.method == 'POST':
        form = BoardForm(request.POST, request.FILES)
        if form.is_valid():
            board = form.save(commit=False)
            board.userprofile = request.user.userprofile
            board.is_active_board = False
            board.save()
            messages.success(request, 'Board created successfully! Pending moderation.')
            return redirect('success_create_page')
    else:
        form = BoardForm()
    context = {
        'form': form
    }
    return render(request, './client/create-board.html', context)

@login_required
def success_create_page(request):
    return render(request, "./client/success-board.html")

@login_required
def update_board_page(request, pk):
    board = get_object_or_404(Board, pk=pk, userprofile__user=request.user)
    if request.method == 'POST':
        form = BoardForm(request.POST, request.FILES, instance=board)
        if form.is_valid():
            form.save()
            messages.success(request, 'Board updated successfully!')
            return redirect('user_boards_page')
    else:
        form = BoardForm(instance=board)
    context = {
        'form': form
    }
    return render(request, './client/update-board.html', context)

@login_required
def delete_board_page(request, pk):
    board = get_object_or_404(Board, pk=pk, userprofile__user=request.user)
    if request.method == 'POST':
        board.delete()
        messages.success(request, 'Board deleted successfully!')
        return redirect('user_boards_page')
    context = {
        'board': board
    }
    return render(request, './client/delete-board.html', context)


@login_required
def create_or_update_profile_page(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!' if not created else 'Profile created successfully!')
            return redirect('profile_page')
    else:
        form = UserProfileForm(instance=profile)
    context = {
        'form': form
    }
    return render(request, './client/create-or-update-profile.html', context)

def logout_action(request):
    logout(request)
    return redirect('home_page')
