showUploadForm = (name) => {
    popup = document.querySelector('.fullWin-container[name="'+name+'"]');
    if(popup.style.display=='block'){
        popup.style.display = 'none'
    }else{
        popup.style.display = 'block'
    }
}

showFollowers = () => {
    followersList = document.querySelector('.followersList')
    followingsList = document.querySelector('.followingsList')
    if( followersList.style.display == 'block'){
        followersList.style.display = 'none';
    }else{
        if( followingsList.style.display == 'block'){
            followingsList.style.display = 'none';
        }
        followersList.style.display = 'block';
    }
}

showFollowings = () => {
    followingsList = document.querySelector('.followingsList')
    followersList = document.querySelector('.followersList')
    if( followingsList.style.display == 'block'){
        followingsList.style.display = 'none';
    }else{
        if( followersList.style.display == 'block'){
            followersList.style.display = 'none';
        }
        followingsList.style.display = 'block';
    }

}