$(document).ready(function() {
    var to = $("#_to")[0];
    var from = $("#_from")[0];
    
    var go1 = $("#go1")[0];
    var go2 = $("#go2")[0];
    
    if ($.jStorage.get('to-fav')) {
        go1.disabled=false;
        to.value = $.jStorage.get('to-fav');
    }
    
    if ($.jStorage.get('from-fav')) {
        go2.disabled=false;
        from.value = $.jStorage.get('from-fav');
    }
    
    to.onchange = function(){
        go1.disabled=false;
        $.jStorage.set('to-fav',to.value);
        
    }
    from.onchange = function(){
        go2.disabled=false;
        $.jStorage.set('from-fav',from.value);
    }
    
});