from django.contrib import admin
from django.urls import path
from . import views
app_name='app'

urlpatterns = [
    path('',views.index,name="index"),
    path('Home/',views.home,name="home"),
    path('Product-Details/<str:type>/<str:desc>/',views.productdetails,name="productdetails"),
    path('Add-Log/<str:type>/<str:desc>/',views.addlog,name="addlog"),
    path('View-All-Logs/<str:type>/<str:desc>/',views.viewalllogs,name="viewalllogs"),
    path('Get-Quantity/',views.getquantity,name="getquantity"),
    path('Get-Remarks/',views.getremarks,name="getremarks"),
    path('Search-Logs/',views.searchlogs,name="searchlogs"),
    path('Search-Product/',views.searchproduct,name="searchproduct"),
    path('User-Logout/',views.user_logout,name="user_logout"),

    path('Export-Individual/<str:type>/<str:desc>/',views.exportindividual,name="exportindividual"),
    path('Export-ALL-Logs/',views.exportalllogs,name="exportalllogs"),
    path('Export-Stock-List/',views.exportstocklist,name="exportstocklist"),
]
