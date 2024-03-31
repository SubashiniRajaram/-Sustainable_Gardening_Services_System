from django.urls import path
from django.contrib import admin

from. import views

urlpatterns = [
    path('',views.home,name='home'),
    path('signin',views.signin ,name='signin'),
    path('signup',views.signup,name='signup'),
    path('postsignin',views.postsignin,name='postsignin'),
    path('postsignup',views.postsignup,name='postsignup'),

    path('category/<str:type>/<str:categorys>/',views.show,name='category'),
    path('products_detail/', views.displayproduct, name='products_detail'),
    path('cart/',views.showcart,name='cart'),
    path('cartremove/', views.remove_from_cart, name='cartremove'),
    path('showcart',views.showCart,name='showcart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('checkout/',views.payment,name='checkout'),
    path('shop',views.shop,name='shop'),


    path('terrace-gardening',views.T_service,name='terrace-gardening'),
    path('terrace-details',views.terrace_details,name='terrace-details'),
    path('terrace-gardening-inquiry',views.terrace_form,name='terrace-gardening-inquiry'),
    path('save_service_detail',views.terrace_save,name='save_service_detail'),
    path('view_summary/<str:service_type>/',views.view_summary,name='view_summary'),
    path('maintainence_home',views.maintainence,name='maintainence_home'),
    path('maintainence',views.maintainence_detail,name='maintainence'),
    path('maintainence-inquiry',views.maintainence_confirm,name='maintainence-inquiry'),
    path('maintainence_service_detail',views.maintainence_save,name='maintainence_service_detail'),
    path('landscaping',views.landscape,name='landscaping'),
    path('landscape-details',views.landscape_details,name='landscape-details'),
    path('landscaping-inquiry',views.landscape_confirm,name='landscaping-inquiry'),
    path('landscape_service_detail',views.landscape_save,name='landscape_service_detail'),

    path('addstatus',views.status,name='addstatus'),
    path('updatesummary',views.update_summary,name='updatesummary'),
    path('payment/', views.payment, name='payment'),



    path('blog',views.blog,name='blog'),
    path('post_detail/<str:id>/',views.post_detail,name='post_detail'),
    path('addpost',views.add_post,name='addpost'),
    path('post_detail/<str:id>/addcomment',views.add_comment,name='addcomment'),
    path('mypost',views.mypost,name='mypost'),
    path('edit/<str:id>/',views.edit_post,name='edit'),
    path('edit/<str:id>/save_edit',views.save_edit,name='save_edit'),
    path('delete/<str:id>/',views.delete,name='delete'),
     path('delete/<str:id>/cancel',views.post_detail,name='cancel'),
     path('delete/<str:id>/confirm_delete',views.delete_post,name='confirm_delete'),
   
    path('fertlizer',views.fertilizer_making),
    path('tutorial',views.tutorial,name='tutorial'),
    path('home_garden',views.video,name='home_garden'),
    path('tips',views.tips,name='tips'),
    path('video',views.tutorial,name='video'),
    path('tutorial_category/<str:type>/',views.tutorial_category,name='tutorial_category'),
    path('tutorial_category2/<str:type>/',views.tips_category,name='tutorial_category2'),
    path('tutorial_category1/<str:type>/',views.gardening_category,name='tutorial_category1'),


     path('infohub',views.info_hub,name='infohub'),
     path('plant_details',views.get_speciesdb,name='plant_details'),
     path('search_plant',views.search_plant,name='search_plant'),
     path('disease_details',views.get_disease_db,name='disease_details'),
     path('guide_detais',views.plants_guide,name='guide_details'),
     path('search_disease',views.search_disease,name='search_disease'),
     path('search_guide',views.search_guide,name='search_guide'),
     path('view_more_species/<str:id>',views.plant_moredetails,name='view_more_species'),
   
     path('suggestion',views.suggestion_home,name='suggestion'),
    path('quiz',views.quiz,name='quiz'),
    path('results_view',views.results,name='results_view'),
    # path('',views.update_plant_data,name=''),

    path('soilcalculator',views.scalculator,name='soil'),
    path('Mulchcalculator',views.mcalculator,name='mulch'),
    path('plantcalculator',views.spcalculator,name='space'),
    path('spacedetails',views.space_details,name='space_details'),

    path('sell',views.sell,name='sell'),
    path('buy',views.buy,name='buy'),
    path('add',views.addwaste,name='addwaste'),
    path('mydonations',views.donation,name='mydonations'),
    path('updatedonation/<str:key>',views.updatedonation,name='updatedonation'),
    path('deletedonation',views.deletedonation,name='deletedonation')





]