$(document).ready(function() {
    var to = $("#_to")[0];
    var from = $("#_from")[0];

    var go1 = $("#go1")[0];
    var go2 = $("#go2")[0];

    var feedback_form = $('#feedback-form')[0];
    var feedback_btn = $('#feedback-btn')[0];
    var feedback_txt = $('#feedback-text')[0];

    if (go1 && go2) { // on index page
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
    }

    if (document.location.pathname == '/route')  {
            if ($.jStorage.get('feedback-sent')) {
                feedback_form.hidden = true;
            }
    }

    if (feedback_btn) { 
            success = function(){
                var txt = 'Спасибо за отзыв!\n';
                if (document.location.pathname == '/route') {
                    txt += 'Если захотите отправить нам что-нибудь ещё, пожалуйста, посетите страницу \"О проекте\"';
                }
                alert(txt);
                $.jStorage.set('feedback-sent',true)
                window.location.replace('/');
            }

            feedback_btn.onclick = function(){
                $.post('/feedback', {'feedback_text' : feedback_txt.value},success)
            }
    }


});