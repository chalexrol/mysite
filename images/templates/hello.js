(function(){
    if (window.bookmarklet !== undefined){
        alert('Window already open');
    }
    else {
        document.body.appendChild(document.createElement('script')).src='https://chalexrol.pythonanywhere.com/static/js/bookmarklet.js?r='+Math.floor(Math.random()*99999999999999999999);
    }
})();