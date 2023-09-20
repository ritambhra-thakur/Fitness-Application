from django.urls import path
from rest_framework.routers import DefaultRouter

from common import views

app_name = "common"

urlpatterns = [
	path("timeline/get/<int:id>/", views.GetTimeline.as_view()),
	path("timeline/list/", views.GetAllTimeline.as_view()),
	path("timeline/update/<int:id>/", views.UpdateTimeline.as_view()),
	path("timeline/create/", views.CreateTimeline.as_view()),
	path("timeline/delete/<int:id>/", views.DeleteTimeline.as_view()),
	#Category
	path("category/get/<int:id>/", views.GetCategory.as_view()),
	path("category/list/", views.GetAllCategory.as_view()),
	path("category/update/<int:id>/", views.UpdateCategory.as_view()),
	path("category/create", views.CreateCategory.as_view()),
	path("category/delete/<int:id>/", views.DeleteCategory.as_view()),
	#Type
	path("type/get/<int:id>/", views.GetType.as_view()),
	path("type/list/", views.GetAllType.as_view()),
	path("type/update/<int:id>/", views.UpdateType.as_view()),
	path("type/create", views.CreateType.as_view()),
	path("type/delete/<int:id>/", views.DeleteType.as_view()),
	# List to get All Numbers
	path("get-all-counts/", views.GetAllNumbersList.as_view()),
	# List to get Profiles
	path("profile/",views.GetProfile.as_view(),),

	#Tags
	path("tags/get-by-owner-id/", views.GetTagsByOwnersIDView.as_view()),

	#Unit
	path("unit/list/", views.GetAllUnitsView.as_view()),
	path("categories_emoji/list/", views.GetAllCategoryEmojiView.as_view()),
	path("type_emoji/list/", views.GetAllTypeEmojiView.as_view()),
	path("message_emoji/list/", views.GetAllMessageEmojiView.as_view()),

	#search
	path("search/<str:search_text>/", views.GlobalSearchView.as_view()),

	#homepage
	path("fetch-homepage-data/", views.HomePageView.as_view()),


]

router = DefaultRouter()

router.register(r'tags', views.TagsViewSets, basename='common')
router.register(r'emoji', views.EmojiViewSets, basename='emoji')
router.register(r'timeline', views.TimeLineViewSets, basename='timeline')


urlpatterns += router.urls