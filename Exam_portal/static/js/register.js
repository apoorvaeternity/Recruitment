/**
 * Created by rupanshu on 4/15/16.
 */

$(document).ready(function (e) {
    // $('input[type="text"][name="StudentNo"]').on("blur", function (e) {
    //     console.log("Blur");
    //     var StudentNo = $(this).val();
    //     var number = StudentNo.slice(0, 6);
    //
    //     if ((StudentNo.length > 8 || StudentNo.length < 7) || isNaN(number)) {
    //
    //         // if(isNaN(number)){
    //         //     console.log('sdsdcdscd');
    //         // }
    //
    //         $(this).addClass("invalid");
    //
    //         alert("Invalid format Student Number");
    //
    //
    //         $(this).focus();
    //         // $(this).focus();
    //
    //
    //     }
    //
    //     $.ajax({
    //         type: "POST",
    //         datatype: 'JSON',
    //         url: "/exam/checkstudent/",
    //         data: {'student_no': StudentNo},
    //         success: function (data) {
    //
    //             console.log(data['message']);
    //             if (data['status']) {
    //                 $('input[type="text"][name="StudentNo"]').addClass("invalid");
    //
    //                 alert(data['message']);
    //
    //
    //                 $('input[type="text"][name="StudentNo"]').focus();
    //
    //                         // $(this).focus();
    //
    //             }
    //
    //         }
    //     })
    //
    //
    // });


    // $('input[type="tel"][name="Contact"]').on("blur", function (e) {
    //     var contact = $(this).val();
    //     console.log(contact);
    //     if (contact.length > 10 || isNaN(contact)) {
    //         $(this).addClass("invalid");
    //         alert("Invalid Mobile number");
    //         $(this).focus();
    //     }
    // });


    $('#endExam').click(function (e) {
        e.preventDefault();
        if (window.confirm("You really want to end the Exam")) {
            window.location.href = "../end";
        }
        else {
            console.log("Studip Person. :/");
        }
    });
});