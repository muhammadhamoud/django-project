from django.urls import path, include
from . import views
app_name = 'blogs'

urlpatterns = [
    # path('blogs/pages/', views.PageListView.as_view(), name='page_list'),
    # path('blogs/featured/', views.FeaturedListView.as_view(), name='page_list'),
    path('blogs/categories/', views.BlogCategoryListView.as_view(), name='category_list'),
    path('blogs/tags/', views.BlogTagListView.as_view(), name='tag_list'),
    path('blogs/posts/', views.PostListView.as_view(), name='post_list'),
    path('blogs/posts/all/', views.PostNameListView.as_view(), name='post_list_all'),
    # path('blogs/posts/search/', views.PostNameListSearchView.as_view(), name='post_list_all'),
    path('blogs/posts/<str:slug>/', views.PostDetailView.as_view(), name='post_detail'),

    # path('blogs/categories/<int:pk>/', views.BlogCategoryDetailView.as_view(), name='category_detail'),

    # path('blogs/dashboard/', views.DashboardView.as_view(), name='dashboard'),
    # path('blogs/users/', views.UserListView.as_view(), name='user_list'),

    # path('blogs/tags/<int:pk>/', views.BlogTagDetailView.as_view(), name='tag_detail'),
]

# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'blogs/blogusers', views.BlogUserViewSet)
# router.register(r'blogs/categories', views.BlogCategoryViewSet)
# router.register(r'blogs/tags', views.BlogTagViewSet)
# router.register(r'blogs/articles', views.ArticleViewSet)
# router.register(r'blogs/history', views.HistoryViewSet)

# urlpatterns += router.urls

# this is for viewset.py ---------------------
# from rest_framework.routers import DefaultRouter
# from rest_framework_nested import routers
# from . import views
# router = DefaultRouter()
# # router.register("posts", views.PostViewSet, basename="posts")
# router.register("posts", views.PostListViewSet, basename="posts")
# posts_router = routers.NestedDefaultRouter(router, "posts", lookup="post")
# router.register("blogscategories", views.CategoryViewSet, basename="blogscategories")
# # router.register("comments", views.CommentViewSet, basename="comments")
# posts_router.register("like", views.LikeViewSet, basename="like")
# posts_router.register("favorite", views.FavoritePostViewSet, basename="favorite")
# posts_router.register("comments", views.CommentViewSet, basename="comments")
# urlpatterns = router.urls + posts_router.urls


