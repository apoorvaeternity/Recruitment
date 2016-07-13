/**
 * Created by rupanshu on 13/7/16.
 */


//submit without marks
//negative more than original marks
$(document).ready(function(e){


    var marks_select= 'input[name="marks"]';
    var negative_select = 'input[name="negative"]';
    var negative_marks = 'input[name="negative_marks"]';
    var marks;
    var negative_value;
    $(negative_marks).attr("disabled","false");

    $(marks_select).attr("required","true");


    $(marks_select).on("blur",function (e) {
        marks = parseInt($(this).val());
        console.log(marks);

    });

    $(negative_select).change(function () {
        $(negative_marks).attr("disabled",!this.checked);
        $(negative_marks).val('');
    });

    $(negative_marks).on("blur",function (e) {
        negative_value = parseInt($(this).val());
        console.log(jQuery.type(negative_value));
        console.log(jQuery.type(marks));

        validate();
    });

    $(marks_select).on("blur",function (e) {
        validate();
    });

    function validate() {
            if(marks <= negative_value){
            $('.error').css("display","block");
            $('.error').text("Negative marks cannot be more than or equals to actual marks");
            console.log(jQuery.type(marks));
            $('#check').attr("disabled","false");

        }else{
            $('.error').css("display","none");
            console.log("ssdcsdcs");
            $('.error').text("");
            $('#check').removeAttr("disabled");
        }
    }








});