from datetime import datetime
import os
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Follow, Profile, Post, likePost
import timeago


@login_required(login_url='login')
def search(request):
    search = request.GET.get('s')
    users = User.objects.filter(username__icontains=search)
    results = set()
    if users:
        for user in users:
            profile = Profile.objects.filter(user=user)
            if profile:
                user.profile = profile
                results.add(user)
    return render(request, 'search.html', {'search':search,'users':results})


# Create your views here.
@login_required(login_url='login')
def index(request):
    users = Profile.objects.all()
    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=user)

    # Show only profile not followed
    check_following = Follow.objects.filter(user=request.user.username)
    followings = [i.following for i in check_following ]
    new_users = set(users)
    for u in users:
        if u.user.username in followings:
            new_users.remove(u)

    posts = Post.objects.all().order_by('-created_at')
    for post in posts:
        f = '%H:%M'
        post.created_a = datetime.strftime(post.created_at,f)
        post.extension = extension(post.image.url)

        created_at = str(post.created_at).split('.')[0]
        post.time_ago = timeago.format(created_at)

        post_user = User.objects.get(username=post.user)
        post.profile = Profile.objects.get(user=post_user)
        # Get likes from likes table
        # post.post_likes = likePost.objects.filter(post_id=post.id).count()

    return render(request, 'index.html', {
        'users':new_users,
        'profile':profile,
        'posts':posts
        })


@login_required(login_url='login')
def profile(request,username=None):
    if username is None:
        return redirect('/profile/'+request.user.username)
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    # Get profile followings
    followings = Follow.objects.filter(user=username).exclude(following=username).all()
    for f in followings:
        f.user = User.objects.get(username=f.following)
        f.profile = Profile.objects.get(user=f.user)
        f.total = Follow.objects.filter(user=f.user.username).count()


    # Get profile followers
    follows = Follow.objects.filter(following=username).all()
    for f in follows:
        f.user = User.objects.get(username=f.user)
        f.profile = Profile.objects.get(user=f.user)
        f.follows = Follow.objects.filter(following=f.user.username).count()


    # Get profile posts
    posts = Post.objects.filter(user=username).order_by('-created_at')
    for post in posts:
        post.extension = extension(post.image.url)
        # created_at = datetime.strftime(post.created_at, )
        created_at = str(post.created_at).split('.')[0]
        post.time_ago = timeago.format(created_at)

    is_following = Follow.objects.filter(user=request.user.username, following=username).first()
    followed = "Unfollow" if is_following else "Follow"
    return render(request, 'profile.html', {
        'profile':profile,
        'posts':posts,
        'follows':follows,
        'followings': followings,
        'followed':followed
        })


@login_required(login_url='login')
def settings(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        # get form data
        
        # check avatar and cover names not to be the same as the default ones
        avatar = profile.avatar if request.FILES.get('avatar') == None else request.FILES.get('avatar')
        cover = profile.cover if request.FILES.get('cover') == None else request.FILES.get('cover')
        
        bio = request.POST['bio']
        location = request.POST['location']
        workingat = request.POST['workingat']
        relationship = request.POST['relationship']
        follow_me = request.POST.get('follow_me')
        private_profile = request.POST.get('private_profile')
        show_online = request.POST.get('show_online')
        allow_comments = request.POST.get('allow_comments')

        # email = request.POST['email']

        # Update profile object
        profile.avatar = avatar
        profile.cover = cover
        profile.bio = bio
        profile.location = location
        profile.workingat = workingat
        profile.relationship = relationship
        profile.follow_me = True if follow_me=='on' else False
        profile.private_profile = True if private_profile=='on' else False
        profile.show_online = True if show_online=='on' else False
        profile.allow_comments = True if allow_comments=='on' else False
        
        # save object into db
        profile.save()

        messages.info(request, 'Your profile has been updated successfully!')
        return redirect('settings')

    return render(request, 'settings.html', {'profile':profile})


@login_required(login_url='login')
def upload(request):
    if request.method == "POST":
        caption = request.POST.get('caption')
        media = request.FILES.get('media')
        if media == None:
            messages.info(request, 'Choose a photo or a video to upload!')
        else:
            user = request.user.username
            post = Post.objects.create(user=user, image=media, caption=caption)
            post.save()
            messages.info(request, 'The post has been uploaded successfully!')
        
        
        return redirect(get_referrer(request))


@login_required(login_url='login')
def like_post(request):
    username = request.user.username
    post_id = request.GET['p']
    post = Post.objects.get(id=post_id)

    check_liked = likePost.objects.filter(post_id=post_id, username=username).first()
    if check_liked is None:
        new_like = likePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.likes += 1
        post.save()
    else:
        check_liked.delete()
        post.likes = post.likes-1 if post.likes>0 else 0
        post.save() 
    return redirect(get_referrer(request))


@login_required(login_url='login')
def delete_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('uid')
        get_post = Post.objects.filter(id=post_id).first()
        if get_post:
            get_post.delete()
        messages.info(request, 'The post has been deleted!')
    return redirect(get_referrer(request))



@login_required(login_url='login')
def follow(request):
    if request.method == "POST":
        user = request.POST.get('user')
        following = request.POST.get('following')
        check = Follow.objects.filter(user=user, following=following).first()
        if check == None and profile != user: 
            new_follow = Follow.objects.create(user=user,following=following)
            new_follow.save()
        else:
            check.delete()

    return redirect(get_referrer(request))

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'The username or password is invalid!')

    return render(request, 'login.html')


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'This email is taken!')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'This Username is Taken!')
                return redirect('signup')
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                user.save()

                # create profile object 
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(
                    user=user_model,
                    id_user = user_model.id
                    )
                new_profile.save()

                #Login user &&  redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                return redirect('settings')
        else:
            messages.info(request, 'Passwords not matching!')
            return redirect('signup')


    return render(request, 'signup.html')
    

def extension(filename):
    name, extension = os.path.splitext(filename)
    if extension in ['.jpg','.jpeg','.png','.webp']:
        return 'photo'
    else:
        return 'video'

def get_referrer(request):
    ref = str(request.META['HTTP_REFERER']).replace('http://'+request.META['HTTP_HOST'],'')
    return '/' if ref == '' else ref