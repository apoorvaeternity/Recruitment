// e.preventDefault();
// var id = $('body > div.container > form > div:nth-child(2)').val();
// console.log(id);
// $.ajax({
//     type: "GET",
//     datatype: 'json',
//     data: {'id': id},
//     url: "http://127.0.0.1:8000/exam/update_question/",
// });


$(document).ready(function (event) {


    $('#excel').hover(function e() {
        $(this).tooltip();
    });


    // $('#excel').click(function(e){
    //     e.preventDefault();
    //     console.log("sending");
    //     $.ajax({
    //         type:"GET",
    //         url:"../studentexcel/",
    //         success:function(status){
    //
    //         }
    //     })
    // });


    $('#delete').click(function (e) {
        e.preventDefault();
        var deleting_id = $('#question > input[type="text"]:nth-child(1)').val();
        if (window.confirm("Really want to delete that  question!")) {
            $.ajax({
                type: "GET",
                datatype: 'json',
                data: {'id': deleting_id},
                url: "http://127.0.0.1:8000/exam/delete/",
                success: function (status) {
                    console.log(status);
                    window.location.href = "../edit";

                }
            });
        } else {
            console.log("stupid admin");
        }

    });


    id_first = $('body > div.container > div > ul > span:nth-child(2) > li').attr('id');
    // console.log(id_first);

    var entry_flag = $("#admin_page_request").val();

    if (entry_flag) {

        console.log(id_first);
        $.ajax({
            type: "GET",
            datatype: 'json',
            data: {'id': id_first},
            url: "http://127.0.0.1:8000/exam/update_question/",
            success: function (data) {
                // console.log("successful request");
                // console.log(data);
                // console.log(data['question']);
                // console.log(data['question_id']);
                // console.log(data['choice']);
                // console.log(data['negative']);
                // console.log(data['negative_marks']);
                // console.log(data['category']);

                question_update(data);
                // $('#id_question').attr("value","Rupanshu");


                // checkmarked(data['radio_checked_key']);
            }
        });


        entry_flag = false;
    }


    function question_update(data) {

        $('#id_question').attr("value", data['question']);
        // $('#id_question').append(data['question']);
        $('#id_question').val('');
        $('#id_question').val($('#id_question').val() + data['question']);

        for (i = 0; i < data['choice'].length; i++) {
            choice_id = "#choice" + (i + 1).toString();
            $(choice_id).attr("value", data['choice'][i][0]);
        }
        $('input[type="number"][name="marks"]').attr("value", data['marks']);
        if (data['negative_marks'] != "" || data['negative_marks'] != 0) {

            $('input[type="checkbox"][name="negative"]').prop("checked", "checked");
            $('input[type="number"][name="negative_marks"]').attr("value", data['negative_marks']);
            console.log("executing true");
        }
        else {
            console.log(data['negative_marks']);
            $('input[type="number"][name="negative_marks"]').attr("value", "");
            $('input[type="checkbox"][name="negative"]').removeAttr("checked");
            console.log("executing false");

        }
        console.log(data['correct_checked']);

        $('#question > input[type="text"]:nth-child(1)').attr("value", data['question_id']);
        var checked_string = "input[type='radio'][value=" + data['correct_checked'] + "]";
        // console.log((checked_string));
        $(checked_string).prop("checked", true);

        //
    }


    console.log(true);
    var entry = 1;
    $('#new_category').click(function (event) {
        event.preventDefault();
        console.log("Hello inside category");

        if ($('#category_list').val() == '' && entry == 1) {
            $('.category').append("<input type='text' name='new_category' placeholder='Name of new category' required/>");
            $('#category_list').attr("disabled", true);
            entry = 0;
        }
        else if (entry == 1) {
            $('.category').append("<input type='text' name='new_category' placeholder='Name of new category' required/>");
            entry = 0;
        }
    });

    $('#category').click(function (e) {
        e.preventDefault();
        var category_id = e.target.id;
        $.ajax({
            type: "GET",
            datatype: "JSON",
            data: {'id': category_id},
            url: "http://127.0.0.1:8000/exam/grid/",
            success: function (data) {
                loaddata(data);
                checkmarked(data['radio_checked_key']);

            }

        });

    });


    //Above Code is for admin panel


    //code for preventing right-click refresh so that the jquery timer wont be refereshed
    // $(document).mousedown(function (e) {
    //     if (e.button == 2) {
    //         e.preventDefault();
    //         return false;
    //     } else {
    //         return true;
    //     }
    // });
    // // $(this).bind("contextmenu", function (e) {
    // //     return false;
    // // });
    // document.onmousedown = disableclick;
    // status = "Right Click Disabled";
    // function disableclick(event) {
    //     if (event.button == 2) {
    //         event.preventDefault();
    //         // alert(status);
    //
    //         return false;
    //     }
    // }


    //-----------------------------------------------------------------------------------

    function disableF5(e) {
        if ((e.which || e.keyCode) == 116) e.preventDefault();
    };
    var flagVal = "";
    var flag = $("#timeStarter");
    if (flag.length > 0) {
        flagVal = flag.val();
    }


    if (flagVal == 'true') {
        disableF5(event);
        $(this).bind("contextmenu", function (e) {
            return false;
        });
        $.ajax({
            type: "GET",
            datatype: 'json',
            url: 'http://127.0.0.1:8000/exam/timer',

            success: function (data) {
                var h = data['time'][0];
                var m = data['time'][1];
                var s = data['time'][2];
                var now = new Date();
                console.log(now.toString());
                var test_time = new Date(now.getFullYear(), now.getMonth(), now.getDate(), h, m, s);
                var epoch = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 0, 0, 0);
                var test_duration = Math.floor((Date.parse(test_time) - Date.parse(epoch)) / 1000);
                console.log(test_duration);
                var today = new Date();
                var stop = setInterval(function () {
                    var current = new Date();
                    var diff = Math.floor((Date.parse(current) - Date.parse(today)) / 1000);
                    console.log(diff);
                    var before_alert = parseInt(data['warn']) * 60;
                    console.log(before_alert);
                    if (diff == test_duration - before_alert) {
                        // alert("about to end");

                        $('#error_message').css("display", "block");

                        // $('#chip').css({"border": "solid 4px red", "padding": "2px"});

                    }

                    if (diff == test_duration) {
                        clearInterval(stop);

                        window.location.replace("http://127.0.0.1:8000/exam/end");

                    }
                    var seconds = diff % 60;
                    var minutes = Math.floor(diff / 60) % 60;
                    var hours = Math.floor(diff / 60 / 60) % 24;


                    document.getElementById("time").innerHTML = hours + ':' + minutes + ':' + seconds;

                }, 1000);
            }
        });
    }


    // for marked and review button
    $('#mark').click(function (event) {
        event.preventDefault();
        console.log(event.target.class);
        console.log("Element have been subitted for mark");
        selectedVal = null;

        var selected = $("input[type='radio'][name='choice']:checked");

        if (selected.length > 0) {
            selectedVal = selected.val();
            console.log(selectedVal);
        }
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8000/exam/next/",
            datatype: 'json',
            data: {'answer': selectedVal},
            success: function (data) {
                console.log("success");
                $('input[type="radio"]').each(function () {
                    $(this).checked = false;
                });
                if (data['color']) {
                    $('#' + data['color'].toString()).css("background-color", '#EC2424');
                }
                else {
                    $('#' + data['color'].toString()).css("background-color", '#EC7724');
                }
                loaddata(data);
                checkmarked(data['radio_checked_key']);
            }
        });


    });


    $('#grid').find('li').click(function (event) {
        event.preventDefault();
        console.log("changing question via grid");
        id = event.target.id;
        console.log(id);
        $.ajax({
            type: "GET",
            datatype: 'json',
            data: {'id': id},
            url: "http://127.0.0.1:8000/exam/grid/",
            success: function (data) {
                console.log("successful request");
                loaddata(data);
                checkmarked(data['radio_checked_key']);
            }
        });
    });

    $('body > div.container > div > ul').find('li').click(function (event) {
        event.preventDefault();
        console.log("updating question via grid");
        id = event.target.id;
        console.log(id);
        var replace = $('#' + id.toString()).val();
        $('#question > label').text("Q" + replace.toString() + ".");

        $.ajax({
            type: "GET",
            datatype: 'json',
            data: {'id': id},
            url: "http://127.0.0.1:8000/exam/update_question/",
            success: function (data) {
                // console.log("successful request");
                // console.log(data);
                // console.log(data['question']);
                // console.log(data['question_id']);
                // console.log(data['choice']);
                // console.log(data['negative']);
                // console.log(data['negative_marks']);
                // console.log(data['category']);

                question_update(data);


                // checkmarked(data['radio_checked_key']);
            }
        });
    });


    $('#previous').click(function (event) {
        event.preventDefault();
        console.log(event.target.class);
        console.log("Element have been subitted for previous");

        //selectedVal = null;
        //
        //var selected = $("input[type='radio'][name='choice']:checked");
        //if (selected.length > 0) {
        //    selectedVal = selected.val();
        //    console.log(selectedVal);
        //}

        $.ajax({
            type: "GET",
            //datatype:'json',
            //data:{'answer':selectedVal},
            url: "http://127.0.0.1:8000/exam/previous/",
            success: function (data) {

                console.log("Ajax on previous have been called");
                console.log(data);
                console.log(data['question']);
                loaddata(data);
                checkmarked(data['radio_checked_key']);


            }
        })
    });


    $('#next').click(function (event) {
        event.preventDefault();
        console.log("Element have been submitted for next ");


        selectedVal = null;

        var selected = $("input[type='radio'][name='choice']:checked");

        if (selected.length > 0) {
            selectedVal = selected.val();
            console.log(selectedVal);
        }
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8000/exam/next/",
            datatype: 'json',
            data: {'answer': selectedVal},
            success: function (data) {

                console.log("success");
                console.log(data);
                console.log(data['question']);
                console.log(data['choices']);
                console.log(data['color']);

                if (data['color']) {
                    $('#' + data['color'].toString()).css("background-color", '#6CB741');
                }
                var color = '#3CC541';
                $('input[type="radio"]').each(function () {
                    $(this).checked = false;
                });
                loaddata(data);
                var color = '#3CC541';

                // $('input[type="radio"]').each(function () {
                //     if($(this).val() == parseFloat(data['radio_checked_key'])){
                //         $(this).attr('checked',true);
                //     }
                // });
                checkmarked(data['radio_checked_key']);


            }

        });

    });
// /
    function checkmarked(key) {
        console.log(key);
        var data = $("input[value=" + key.toString() + "]")
        data.prop("checked", true);
        console.log("inside that function" + data);
    }


    function loaddata(data) {

        console.log(data['negative']);

        if (data['negative'] == true) {
            var negative = "*";

        }
        else {
            var negative = "";
        }
        // $("#negative").text(negative.color("red"));

        $('#question').text(data['question_no'] + ". " + data['question'] + negative);

        console.log(data['choice_data'][0][0]);
        console.log(data['choice_data'][0][1]);
        console.log("hello " + data['question_no'].toString());
        // $('#choices').text(" ")

        console.log("checked data");
        console.log(data['radio_checked_key']);

        // radio_string ="input[type='radio'][name='choice'][value="+data['radio_checked_key'].toString()+"]"
        // console.log(radio_string);
        // $(radio_string).prop('checked',true);
        // $('span #question_no').text(data['question_no'] + ".");


        for (i = 0; i < data['choice_data'].length; i++) {

            id = '#q' + (i + 1).toString();
            $('#test' + (i + 1).toString()).attr({'value': data['choice_data'][i][1], 'checked': false});
            $(id).text(data['choice_data'][i][0]);

            // $('#choices').append('<li class="collection=item"><input name="choice" type="radio" id="test"' + toString(i + 1) + 'value="' + toString(data['choice_data'][i][1]) + '"/><label style="color:black;font-style: normal;" for="test' + toString(i + 1) + '" id="q' + toString(i + 1) + '">' + data['choice_data'][i][0] + '</label></li>');

        }

        if (data['radio_checked_key']) {
            var input_string = "#choices > li[id=" + data['radio_checked_key'].toString() + "]";
            console.log("Executing inside that loaddata");
            $(input_string).find('input').prop("checked", true);

        }

    }


    // CSRF code
    function getCookie(name) {
        var cookieValue = null;
        var i = 0;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


});
