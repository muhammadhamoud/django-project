from django.urls import path

from settings.view.menu import  settings_menu_items_view, settings_menu_list_view

# from settings.views.segments import (
#     DetailSegmentCreateView,
#     DetailSegmentUpdateView,
#     SegmentMappingTableView,
#     SubSegmentMappingTableView,
#     DetailSegmentMappingTableView,
# )

app_name = "settings"


from django.urls import path
from view.segments import (
    segment_group_manage_view
)
from settings.view.views import segment_category_view, segment_group_view

urlpatterns = [
    path("settings-main/", settings_menu_list_view, name="settings_main"),
    
    path("settings-menu/", settings_menu_list_view, name="menu_list"),
    path("settings-menu/<slug:slug>/", settings_menu_items_view, name="menu_items"),
    
    
    # path("segment-groups/manage/", segment_group_manage_view, name="segment-group-manage"),
    path("segment-groups/", segment_group_view, name="segment-group"),
    path("segment-category/", segment_category_view, name="segment-category"),



]



urlpatterns += [
    # path("mapping/", SegmentMappingTableView.as_view(), name="mapping-table"),
    # path("mapping/subsegments/", SubSegmentMappingTableView.as_view(), name="subsegment-mapping-table"),
    # path("mapping/detailsegments/", DetailSegmentMappingTableView.as_view(), name="detailsegment-mapping-table"),

    # path("detailsegments/create/assign/", DetailSegmentCreateView.as_view(), name="detailsegment-assign-create"),
    # path("detailsegments/<int:pk>/assign/edit/", DetailSegmentUpdateView.as_view(), name="detailsegment-assign-update"),
]


# from .views import (
#     SegmentGroupListView,
#     SegmentGroupCreateView,
#     SegmentGroupUpdateView,
#     SegmentGroupDeleteView,
#     SegmentCreateView,
#     SegmentUpdateView,
#     SegmentDeleteView,
#     SubSegmentCreateView,
#     SubSegmentUpdateView,
#     SubSegmentDeleteView,
#     DetailSegmentCreateView,
#     DetailSegmentUpdateView,
#     DetailSegmentDeleteView,
# )

# urlpatterns = [
#     path("segments/", SegmentGroupListView.as_view(), name="group-list"),

#     path("groups/create/", SegmentGroupCreateView.as_view(), name="group-create"),
#     path("groups/<int:pk>/edit/", SegmentGroupUpdateView.as_view(), name="group-update"),
#     path("groups/<int:pk>/delete/", SegmentGroupDeleteView.as_view(), name="group-delete"),

#     path("segments/create/", SegmentCreateView.as_view(), name="segment-create"),
#     path("segments/<int:pk>/edit/", SegmentUpdateView.as_view(), name="segment-update"),
#     path("segments/<int:pk>/delete/", SegmentDeleteView.as_view(), name="segment-delete"),

#     path("subsegments/create/", SubSegmentCreateView.as_view(), name="subsegment-create"),
#     path("subsegments/<int:pk>/edit/", SubSegmentUpdateView.as_view(), name="subsegment-update"),
#     path("subsegments/<int:pk>/delete/", SubSegmentDeleteView.as_view(), name="subsegment-delete"),

#     path("detailsegments/create/", DetailSegmentCreateView.as_view(), name="detailsegment-create"),
#     path("detailsegments/<int:pk>/edit/", DetailSegmentUpdateView.as_view(), name="detailsegment-update"),
#     path("detailsegments/<int:pk>/delete/", DetailSegmentDeleteView.as_view(), name="detailsegment-delete"),
# ]