from django.conf.urls import url, handler404

from . import views
from . import ajax

# app_name = 'Exam_portal'

urlpatterns = [
    url(r'^register/$', views.register, name="register"),
    url(r'^list/$', views.ListQuestion.as_view(), name='list'),
    url(r'^instruction/$', views.instruction, name="instruction"),
    url(r'^show/$', views.show, name="ajaxshow"),
    url(r'^next/$', ajax.ajaxnext, name="ajaxnext"),
    url(r'^previous/$', ajax.ajaxprevious, name="ajaxprevious"),
    url(r'^postajax/$', ajax.postajax, name="postajax"),
    url(r'^grid/$', ajax.grid, name="ajaxgrid"),
    url(r'^timer/$', views.timer, name='timer'),
    url(r'^end/$', views.end, name="end"),
    url(r'^admin/$', views.admin, name="admin"),
#    url(r'^edit/$', views.edit_question, name="edit_question"),
    url(r'^update_question/$', ajax.question_update, name="question_update"),
    url(r'^delete/$', ajax.delete, name="delete"),
    url(r'^adminchoice/$', views.adminchoice, name="adminchoice"),
    url(r'^edittime/$', views.edittime, name="edittime"),
    url(r'^student_section/$', views.student_section, name="student"),
    url(r'^adminLogin/$', views.admin_auth, name="admin_auth"),
    url(r'^adminLogout/$', views.logout_admin, name="logout_admin"),
    url(r'^download/$', ajax.excel, name="excel"),
    url(r'^review/$', views.review, name="review"),
    url(r'^switch/$', views.exam_starter_switch, name="switch"),
    url(r'^notstarted/$', views.not_started, name="notstarted"),
    url(r'^check_grid/$', ajax.check_grid, name="check_grid"),
    url(r'^login/$', views.login, name="login"),
    url(r'^refresh/$', views.refresh, name="refresh"),
    url(r'^category/$', views.add_category, name="category"),
    url(r'^questionlist/$', views.question_list, name="question_list"),
    url(r'^questionupdate/(?P<pk>[0-9]+)/$', views.question_edit, name="question_edit"),
    url(r'^graph/(?P<id>[0-9]+)/$', views.graph, name="graph"),

]
