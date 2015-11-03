$(document).ready(function() {

    var _to_button = $("#_to_button")[0];
    var _from_button = $("#_from_button")[0];

    var to = $("#_to")[0];
    var from = $("#_from")[0];

    var go1 = $("#go1")[0];
    var go2 = $("#go2")[0];

    var feedback_form = $('#feedback-form')[0];
    var feedback_btn = $('#feedback-btn')[0];
    var feedback_txt = $('#feedback-text')[0];

    var date_radio_selector = $('#date-radio-selector')[0];
    var time_radio_selector = $('#time-radio-selector')[0];

    var time_labels = $('.time-option-label');
    var time_options = $('input[name=time_options]');

    if (go1 && go2) { // on index page
            _to_button.onclick = function(){
                if ($("#to-edu-from")[0].value == "dubki")
                {
                    _to_button.innerText = "Одинцово";
                    $("#to-edu-from")[0].value = "odintsovo";
                }
                else if ($("#to-edu-from")[0].value == "odintsovo"){
                    _to_button.innerText = "Дубков";
                    $("#to-edu-from")[0].value = "dubki";
                }
            };

            _from_button.onclick = function(){
                if ($("#to-dorm-to")[0].value == "dubki")
                {
                    _from_button.innerText = "Одинцово";
                    $("#to-dorm-to")[0].value = "odintsovo";
                }
                else if ($("#to-dorm-to")[0].value == "odintsovo"){
                    _from_button.innerText = "Дубки";
                    $("#to-dorm-to")[0].value = "dubki";
                }
            };

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
            };

            from.onchange = function(){
                go2.disabled=false;
                $.jStorage.set('fav-station',from.value);
            };


    }

    if (document.location.pathname == '/')  {
            date_radio_selector.style.display = 'block';
            time_radio_selector.style.display = 'none';
            $('input[name=date_options]')[0].checked = true;
    }

    if (date_radio_selector) {
                var now = new Date();
                if (now.getHours() >= 19) {
                    $('.date-today-label')[0].style.display = 'none';
                } // FIXME hardcoded :(
                date_radio_selector.onchange = function() {
                        var date_value = $('input[name=date_options]:checked').val();
                        date_radio_selector.style.display = 'none';
                        time_radio_selector.style.display = 'block';

                        if (date_value == 'today')
                        {
                            $(".time-option-label, input[name=time_options]").css("display","none")
                            var _arrival = new Date();
                            var _departure = new Date();
                            var _now = new Date();
                            var Response = $.post('/route_json', {'_from': $("#to-edu-from")[0].value, '_to': $('#_to')[0].value}, success = 
                                function() {
                                        var Parsed = JSON.parse(Response.responseText);
                                        var _h = Parsed['arrival']['hour'];
                                        var _m = Parsed['arrival']['minute'];
                                         _arrival.setHours(_h);
                                        _arrival.setMinutes(_m);

                                        _h = Parsed['departure']['hour'];
                                        _m = Parsed['departure']['minute'];
                                         _departure.setHours(_h);
                                        _departure.setMinutes(_m);
   
                                        // remove the past times
                                for (var i = 0; i < time_options.length; i++) {
                                var cur_date = new Date();
                                var h = parseInt(time_options[i].value.split(':')[0]);
                                var m = parseInt(time_options[i].value.split(':')[1]);
                                cur_date.setHours(h);
                                cur_date.setMinutes(h);
                                if (cur_date >= _arrival && _departure >= _now)
                                {
                                    time_labels[i].style.display = 'block';
                                    time_options[i].style.display = 'block';
                                }
                            };

                           

                            
                            });
                        }
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