from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^index$', views.index),
    url(r'^new_user$', views.new_user),
    url(r'^old_user$', views.old_user),
    url(r'^add_favorite/([0-9]+)$', views.add_favorite),
    url(r'^remove_favorite/([0-9]+)$', views.remove_favorite), 
    url(r'^new_quote$', views.new_quote),
    url(r'^from_zero$', views.from_zero),
    # url(r'^total_reset$', views.total_reset),
    url(r'^quotes$', views.quotes),
    url(r'^user_selected/([0-9]+)$', views.user_selected),
    url(r'^clearance$', views.clearance),
    url(r'^$', views.index),
    url(r'^logout$', views.logout), 
    # url(r'^rand_word$', views.rand_word),
    #  url(r'^result$', views.result),
    # This line has changed! Notice that urlpatterns is a list, the comma is in
]                            # anticipation of all the routes that will be coming soon