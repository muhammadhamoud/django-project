from django.urls import path
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

urlpatterns = [
    path("segment-groups/manage/", segment_group_manage_view, name="segment-group-manage"),
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