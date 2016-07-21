/**
 * Created by rupanshu on 4/15/16.
 */

$(document).ready(function (e) {


    $('#endExam').click(function (e) {
        e.preventDefault();
        if (window.confirm("You really want to end the Exam")) {
            window.location.href = "../review/";
        }
    });
});