$(document).ready(function() {
    var to = $("#_to")[0];
    var from = $("#_from")[0];

    var go1 = $("#go1")[0];
    var go2 = $("#go2")[0];

    if ($.jStorage.get('fav-station')) {
        go1.disabled=false;
        to.value = $.jStorage.get('fav-station');
    }

    if ($.jStorage.get('fav-station')) {
        go2.disabled=false;
        from.value = $.jStorage.get('fav-station');
    }

    to.onchange = function(){
        go1.disabled=false;
        $.jStorage.set('fav-station',to.value);

    }
    from.onchange = function(){
        go2.disabled=false;
        $.jStorage.set('fav-station',from.value);
    }

});