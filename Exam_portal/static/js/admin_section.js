/**
 * Created by rupanshu on 13/7/16.
 */

var marks_select = 'input[name="marks"]';
var negative_select = 'input[name="negative"]';
var negative_marks = 'input[name="negative_marks"]';
var marks;
var negative_value;
var form_time = 'input[name="minutes"]'
var warn_time = 'input[name="warn"]'

//------------------ disable refresh on f5;


function disableButtonsDown(e) {
    if ((e.which || e.keyCode) == 116) e.preventDefault();
}
$(document).on("keydown", disableButtonsDown);

//--------------------



$(document).ready(function (e) {

    $('#time_form').off("submit");

    $("#question_form").off("submit");


    function validate_time(){
        
        var time1 = parseInt($(form_time).val());
        var time2 = parseInt($(warn_time).val());
        var time_name = $('#test_name').val();

        if (time_name.toString().length > 20){
            $('#time_error').text("Invalid test name length");
            return false;

        }

        if (isNaN(time1) && isNaN(time2)){
            $('#time_error').text("Only Integer Values are allowed");
            return false;
        }
        if( time1 < time2){
            $('#time_error').text("Prompt time cannot be greater the Exam time.");
            return false;
        }
        if( time1 < 0  && time2 < 0){
            $('#time_error').text("Time cannot be negative");
            return false;
        }
        if(time1 > 1440 && time1 > 1440 ){
            $('#time_error').text("Invalid Length");
            return false;
        }

        return true;
    }

    $('#time_form').on("submit",function (e){
        if(!validate_time()){
            e.preventDefault();
        }
    });


    function validate_marks(){
        marks = parseInt($(marks_select).val());
        negative_value = parseInt($(negative_marks).val());
        console.log(marks);
        console.log(negative_value);

        if(marks <= 0){
            $('.error').css("display", "block");
            $('.error').text("Marks cannot be negative");
            return false;
        }
        if (marks <= negative_value){
            console.log("error");
            $('.error').css("display", "block");
            $('.error').text("Negative marks cannot be more than or equals to actual marks");
            return false;
        }

        var c1 = $("#choice1").val();
        var c2 = $("#choice2").val();
        var c3 = $("#choice3").val();
        var c4 = $("#choice4").val();
        console.log(c1);

        if( c1 == c2 ){
            $('#same_error').text("Choices could Not be Same");
            return false;

        }
        else if(c1 == c3){
            $('#same_error').text("Choices could Not be Same");
            return false;
        }
        else if(c1 == c4){
            $('#same_error').text("Choices could Not be Same");
            return false;
        }
        else if(c2 == c3){
            $('#same_error').text("Choices could Not be Same");
            return false;
        }
        else if(c2 == c4){
            $('#same_error').text("Choices could Not be Same");
            return false;
        }
        else if(c3 == c4){
            $('#same_error').text("Choices could Not be Same");
            return false;
        }

        if(marks)
        if (negative_value<0){
            $('.error').css("display", "block");
            $('.error').text("Negative sign is not allowed");
            return false;
        }

        return true;

    }

    $("#question_form").on("submit",function (e) {
        if(!validate_marks()){
            e.preventDefault();
        }
    });

    // $('form').submit(function (e) {
    //
    //     marks = parseInt($(marks_select).val());
    //     negative_marks = parseInt($(negative_marks).val());
    //
    //     if (validate()) {
    //         console.log("preventing default");
    //         // e.preventDefault();
    //     }
    //     else {
    //         e.preventDefault();
    //     }
    // });


    // $(marks_select).on("blur", function (e) {
    //     marks = parseInt($(this).val());
    //     console.log(marks);
    //     console.log(window.location.href);
    //     negative_value = parseInt($(negative_marks).val());
    //
    // });
    //
    $(negative_select).change(function () {

        console.log(this.checked);

        if ($(negative_marks).val() == 0) {
            $(negative_marks).removeAttr('disabled');
            $('.error').css("display",'none');
        }


        console.log($(negative_marks).prop("val"));

        if (this.checked) {
            $(negative_marks).removeAttr("disabled")
            $(negative_marks).prop("required",true);
        }

        if (!this.checked) {
            $(negative_marks).attr("disabled",!this.checked);
        }

        $(negative_marks).val(null);


    });
    //
    // $(negative_marks).on("blur", function (e) {
    //     negative_value = parseInt($(this).val());
    //     console.log(jQuery.type(negative_value));
    //     console.log(jQuery.type(marks));
    //
    //     validate();
    // });
    //
    // $(marks_select).on("blur", function (e) {
    //     validate();
    // });
    //
    // function validate() {
    //     if (marks <= negative_value) {
    //         $('.error').css("display", "block");
    //         $('.error').text("Negative marks cannot be more than or equals to actual marks");
    //         console.log(jQuery.type(marks));
    //         $('#check').attr("disabled", "false");
    //         return false;
    //     } else {
    //         $('.error').css("display", "none");
    //         console.log("ssdcsdcs");
    //         $('.error').text("");
    //         $('#check').removeAttr("disabled");
    //         return true;
    //     }
    // }


});