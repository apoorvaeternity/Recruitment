/**
 * Created by rupanshu on 4/15/16.
 */

$(document).ready(function(e){
    $('input[type="text"][name="StudentNo"]').on("blur",function (e){
        console.log("Blur");
        var StudentNo = $(this).val();
        if(StudentNo.length > 7 || StudentNo.length < 5){
            $(this).addClass("invalid");
            alert("invalid length of Stundent Number");
            $(this).focus();
            // $(this).focus();
        }
    });



    $('input[type="tel"][name="Contact"]').on("blur",function (e) {
        var contact = $(this).val();
        console.log(contact);
        if(contact.length>10 || isNaN(contact)){
            $(this).addClass("invalid");
            alert("Invalid Mobile number");
            $(this).focus();
        }
    });


    $('#endExam').click(function(e){
        e.preventDefault();
        if(window.confirm("You really want to end the Exam")){
            window.location.href = "../end";
        }
        else{
            console.log("Studip Person. :/");
        }
    });
});