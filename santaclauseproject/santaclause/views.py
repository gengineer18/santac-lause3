from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from . import models
from .models import Present, User, Profile
from .forms import SignupForm, ProfileEditForm, AccountEditForm, PresentForm

# SQL_SEL_PRESENT_1 = 'SELECT * FROM present ' \
#                     'INNER JOIN profile ON present.user_id = profile.user_id ' \
#                     'order by present.id desc'


def paginate_queryset(request, queryset, count):  # ページング処理
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj


def index(request):  # インデックスページ
    # presents = Present.objects.raw(SQL_SEL_PRESENT_1)
    presents = Present.objects.select_related().all()
    page_obj = paginate_queryset(request, presents, 5)
    context = {
        'presents': page_obj.object_list,
        'page_obj': page_obj
    }
    return render(request, 'santaclause/index.html', context)


def signup(request):  # 新規登録ページ
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('santaclause:index')
    else:
        form = SignupForm()
    return render(request, 'santaclause/signup.html', {'form': form})


@login_required
def present(request):  # プレゼント(投稿)ページ
    if request.method == 'POST':
        form = PresentForm(request.POST, request.FILES)
        if not form.is_valid():
            raise ValueError('invalid')
        if form.cleaned_data['image1']:
            image1 = form.cleaned_data['image1']
        else:
            image1 = None
        if form.cleaned_data['image2']:
            image2 = form.cleaned_data['image2']
        else:
            image2 = None
        if form.cleaned_data['image3']:
            image3 = form.cleaned_data['image3']
        else:
            image3 = None

        present = Present.objects.create(
            user_id=request.user.id,
            conclusion=request.POST['conclusion'],
            title=request.POST['title'],
            image1=image1,
            topic1=request.POST['topic1'],
            contents1=request.POST['contents1'],
            topic2=request.POST['topic2'],
            image2=image2,
            contents2=request.POST['contents2'],
            topic3=request.POST['topic3'],
            image3=image3,
            contents3=request.POST['contents3']
        )

        return redirect('santaclause:detail', present.pk)
    return render(request, 'santaclause/present.html', {'form': PresentForm()})


def detail(request, pk):  # プレゼント(投稿)詳細ページ
    detail = get_object_or_404(Present, pk=pk)
    present = Present.objects.get(pk=pk)
    profile = Profile.objects.get(user_id=present.user_id)
    d = {
        'present': present,
        'profile': profile
    }
    return render(request, 'santaclause/detail.html', d)


@login_required
def edit(request, pk):  # プレゼント(投稿)修正ページ
    try:
        present = models.Present.objects.get(pk=pk)
    except models.Present.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = PresentForm(request.POST, request.FILES)
        if not form.is_valid():
            raise ValueError('Value Error Occurred')

        if form.cleaned_data['image1']:
            image1 = form.cleaned_data['image1']
        else:
            if present.image1:
                image1 = present.image1
            else:
                image1 = None
        if form.cleaned_data['image2']:
            image2 = form.cleaned_data['image2']
        else:
            if present.image2:
                image2 = present.image2
            else:
                image2 = None
        if form.cleaned_data['image3']:
            image2 = form.cleaned_data['image3']
        else:
            if present.image3:
                image3 = present.image3
            else:
                image3 = None

        present.title = request.POST['title']
        present.conclusion = request.POST['conclusion']
        present.topic1 = request.POST['topic1']
        present.image1 = image1
        present.contents1 = request.POST['contents1']
        present.topic2 = request.POST['topic2']
        present.image2 = image2
        present.contents2 = request.POST['contents2']
        present.topic3 = request.POST['topic3']
        present.image3 = image3
        present.contents3 = request.POST['contents3']
        present.save()

        return redirect('santaclause:detail', pk)
    else:
        form = PresentForm(initial={
            'title': present.title,
            'conclusion': present.conclusion,
            'topic1': present.topic1,
            'image1': present.image1,
            'contents1': present.contents1,
            'topic2': present.topic2,
            'image2': present.image2,
            'contents2': present.contents2,
            'topic3': present.topic3,
            'image3': present.image3,
            'contents3': present.contents3,
        })
    return render(request, 'santaclause/edit.html', {'form': form})


@login_required
def delete(request, pk):  # プレゼント(投稿)削除処理
    try:
        present = models.Present.objects.get(pk=pk)
    except models.Present.DoesNotExist:
        raise Http404
    present.delete()
    return redirect('santaclause:index')


@login_required
def api_favorite(request, pk):  # お気に入り処理
    try:
        present = models.Present.objects.get(pk=pk)
    except models.Present.DoesNotExist:
        raise Http404
    present.favorite += 1
    present.save()
    return JsonResponse({"favorite": present.favorite})


@login_required
def user_info(request, pk):  # ユーザープロフィール情報ページ
    try:
        user_info = models.User.objects.get(pk=pk)
    except models.Present.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        return redirect('santaclause:profile_edit', pk)
    else:
        d = {
            'user': User.objects.get(pk=pk),
            'profile': Profile.objects.get(user_id=pk),
        }
        return render(request, 'santaclause/user_info.html', d)


@login_required
def profile_edit(request, pk):  # ユーザープロフィール編集ページ
    try:
        profile = models.Profile.objects.get(user_id=pk)
    except models.Present.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES)
        if not form.is_valid():
            raise ValueError('不正なデータが入力されました')

        profile.introduce = request.POST['introduce']
        profile.location = request.POST['location']
        profile.web_site = request.POST['web_site']
        if form.cleaned_data['icon']:  # 画像を更新する場合は新規画像を設定
            profile.icon = form.cleaned_data['icon']
        else:
            if not profile.icon == 'user/image/default_icon.png':  # デフォルト以外の画像を既に使用している場合は更新しない
                profile.icon = profile.icon
            else:
                profile.icon = 'user/image/default_icon.png'  # デフォルト画像から更新しない場合

        profile.save()

        return redirect('santaclause:user_info', pk)

    else:
        form = ProfileEditForm(initial={
            'introduce': profile.introduce,
            'location': profile.location,
            'web_site': profile.web_site,
            'icon': profile.icon
        })
    return render(request, 'santaclause/user_edit.html', {'form': form})


@login_required
def account_info(request, pk):  # アカウント情報ページ
    try:
        user_info = models.User.objects.get(pk=pk)
    except models.Present.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
        return redirect('santaclause:account_edit', pk)
    else:
        d = {
            'user': User.objects.get(pk=pk),
             }
    return render(request, 'santaclause/account_info.html', d)


@login_required
def account_edit(request, pk):  # アカウント情報編集ページ
    try:
        user = models.User.objects.get(pk=pk)
    except models.Present.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = AccountEditForm(request.POST or None, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('santaclause:account_info', pk)
    else:
        form = AccountEditForm(initial={
            'username': user.username,
            'email': user.email,
        })
    return render(request, 'santaclause/account_edit.html', {'form': form})
