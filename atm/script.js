function timeRefresh(time) {
    document.documentElement.requestFullscreen();
    setTimeout("location.reload(true);", time)
}