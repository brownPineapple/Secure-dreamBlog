from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from posts.views import PostListView, PostCreateView

from posts.views import profile, register_view, logout_view, login_view, index, blog, post, search, post_update, post_delete, post_create
#import debug_toolbar


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login_page'),
    path('', PostListView.as_view(), name='index_page'),
    path('register/', register_view, name='signup_page'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('blog/', blog, name='post_list'),
    path('search/', search, name='search'),
    path('post/<int:id>/', post, name='post_detail'),
    #path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('create/', post_create, name='post_create'),
    #path('create/', PostCreateView, name='post_create'),
    path('post/<int:id>/update', post_update, name='post_update'),
    path('post/<int:id>/delete', post_delete, name='post_delete'),
    path('tinymce/', include('tinymce.urls')),
    #path('__debug__/', include(debug_toolbar.urls)),
]

if settings.DEBUG:

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
