/**
 * Created by rupanshu on 13/7/16.
 */


//submit without marks
//negative more than original marks
var marks_select = 'input[name="marks"]';
var negative_select = 'input[name="negative"]';
var negative_marks = 'input[name="negative_marks"]';
var marks;
var negative_value;
var path_name = window.location.pathname


//------------------ disable refresh on f5;


// function disableButtonsDown(e) {
//     if ((e.which || e.keyCode) == 116) e.preventDefault();
// };
// $(document).on("keydown", disableButtonsDown);
//
// //--------------------

$(document).ready(function (e) {


    if(path_name == '/exam/edit/'){
        $(negative_marks).removeAttr('disabled');
    }

    if($(negative_select).prop("checked")){
        console.log("its checked");
    }
    



    $('form').on('keyup keypress', function (e) {
        var keyCode = e.keyCode || e.which;
        if (keyCode === 13) {
            e.preventDefault();
            return false;
        }
    });


    $('form').submit(function (e) {

        marks = parseInt($(marks_select).val());
        negative_marks = parseInt($(negative_marks).val());

        if (validate()) {
            console.log("preventing default");
            // e.preventDefault();
        }
        else {
            e.preventDefault();
        }
    });


    $(marks_select).on("blur", function (e) {
        marks = parseInt($(this).val());
        console.log(marks);
        console.log(window.location.href);
        negative_value = parseInt($(negative_marks).val());

    });

    $(negative_select).change(function () {

        console.log(this.checked);

        if ($(negative_marks).val() == 0) {
            $(negative_marks).removeAttr('disabled');
            $('.error').css("display",'none');
        }

        if (this.checked == true) {
            $('#check').removeAttr("disabled");
        }


        $(negative_marks).attr("disabled", !this.checked);
        $(negative_marks).val(null);


    });

    $(negative_marks).on("blur", function (e) {
        negative_value = parseInt($(this).val());
        console.log(jQuery.type(negative_value));
        console.log(jQuery.type(marks));

        validate();
    });

    $(marks_select).on("blur", function (e) {
        validate();
    });

    function validate() {
        if (marks <= negative_value) {
            $('.error').css("display", "block");
            $('.error').text("Negative marks cannot be more than or equals to actual marks");
            console.log(jQuery.type(marks));
            $('#check').attr("disabled", "false");
            return false;
        } else {
            $('.error').css("display", "none");
            console.log("ssdcsdcs");
            $('.error').text("");
            $('#check').removeAttr("disabled");
            return true;
        }
    }


});