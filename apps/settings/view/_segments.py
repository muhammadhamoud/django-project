
# from django.contrib import messages
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.exceptions import PermissionDenied
# from django.shortcuts import redirect
# from django.urls import reverse
# from django.views.generic import TemplateView

# from properties.models import Property
# from ..forms._segments import DetailSegmentAssignmentForm, SegmentFormSet, SubSegmentFormSet, DetailSegmentFormSet
# from ..models.segments import Segment, SubSegment, DetailSegment
# from accounts.models import UserPropertyAccessMixin


# class SegmentMappingTableView(LoginRequiredMixin, UserPropertyAccessMixin, TemplateView):
#     template_name = "mappings/mapping_table.html"
#     formset_class = SegmentFormSet
#     queryset_model = Segment
#     title = "Segment Mapping"
#     table_type = "segment"

#     def get_queryset(self, property_obj):
#         return self.queryset_model.objects.filter(
#             group__property=property_obj
#         ).select_related("group").order_by("group__sort_order", "sort_order", "name")

#     def get_formset(self, property_obj, data=None):
#         return self.formset_class(
#             data=data,
#             queryset=self.get_queryset(property_obj),
#             form_kwargs={"property_obj": property_obj},
#             prefix=self.table_type,
#         )

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         selected_property = self.get_selected_property()
#         context["allowed_properties"] = self.get_allowed_properties()
#         context["selected_property"] = selected_property
#         context["title"] = self.title
#         context["table_type"] = self.table_type
#         context["formset"] = kwargs.get("formset") or self.get_formset(selected_property)
#         return context

#     def post(self, request, *args, **kwargs):
#         selected_property = self.get_selected_property()
#         formset = self.get_formset(selected_property, data=request.POST)

#         if formset.is_valid():
#             instances = formset.save(commit=False)

#             for obj in formset.deleted_objects:
#                 obj.delete()

#             for instance in instances:
#                 instance.save()

#             messages.success(request, f"{self.title} updated successfully.")
#             return redirect(f"{reverse('mappings:mapping-table')}?property={selected_property.id}")

#         context = self.get_context_data(formset=formset)
#         return self.render_to_response(context)


# class SubSegmentMappingTableView(SegmentMappingTableView):
#     formset_class = SubSegmentFormSet
#     queryset_model = SubSegment
#     title = "SubSegment Mapping"
#     table_type = "subsegment"

#     def get_queryset(self, property_obj):
#         return self.queryset_model.objects.filter(
#             segment__group__property=property_obj
#         ).select_related("segment", "segment__group").order_by(
#             "segment__group__sort_order", "segment__sort_order", "sort_order", "name"
#         )

#     def post(self, request, *args, **kwargs):
#         selected_property = self.get_selected_property()
#         formset = self.get_formset(selected_property, data=request.POST)

#         if formset.is_valid():
#             instances = formset.save(commit=False)

#             for obj in formset.deleted_objects:
#                 obj.delete()

#             for instance in instances:
#                 instance.save()

#             messages.success(request, f"{self.title} updated successfully.")
#             return redirect(f"{reverse('mappings:subsegment-mapping-table')}?property={selected_property.id}")

#         context = self.get_context_data(formset=formset)
#         return self.render_to_response(context)


# class DetailSegmentMappingTableView(SegmentMappingTableView):
#     formset_class = DetailSegmentFormSet
#     queryset_model = DetailSegment
#     title = "Detail Segment Mapping"
#     table_type = "detailsegment"

#     def get_queryset(self, property_obj):
#         return self.queryset_model.objects.filter(
#             sub_segment__segment__group__property=property_obj
#         ).select_related("sub_segment", "sub_segment__segment", "sub_segment__segment__group").order_by(
#             "sub_segment__segment__group__sort_order",
#             "sub_segment__segment__sort_order",
#             "sub_segment__sort_order",
#             "sort_order",
#             "name",
#         )

#     def post(self, request, *args, **kwargs):
#         selected_property = self.get_selected_property()
#         formset = self.get_formset(selected_property, data=request.POST)

#         if formset.is_valid():
#             instances = formset.save(commit=False)

#             for obj in formset.deleted_objects:
#                 obj.delete()

#             for instance in instances:
#                 instance.save()

#             messages.success(request, f"{self.title} updated successfully.")
#             return redirect(f"{reverse('mappings:detailsegment-mapping-table')}?property={selected_property.id}")

#         context = self.get_context_data(formset=formset)
#         return self.render_to_response(context)


# from django.views.generic import CreateView, UpdateView

# class DetailSegmentCreateView(LoginRequiredMixin, UserPropertyAccessMixin, CreateView):
#     model = DetailSegment
#     form_class = DetailSegmentAssignmentForm
#     template_name = "mappings/detailsegment_assignment_form.html"

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs["allowed_properties"] = self.get_allowed_properties()
#         return kwargs

#     def get_success_url(self):
#         property_id = self.object.property.id
#         return reverse("mappings:group-list") + f"?property={property_id}"


# class DetailSegmentUpdateView(LoginRequiredMixin, UserPropertyAccessMixin, UpdateView):
#     model = DetailSegment
#     form_class = DetailSegmentAssignmentForm
#     template_name = "mappings/detailsegment_assignment_form.html"

#     def get_queryset(self):
#         return DetailSegment.objects.filter(
#             sub_segment__segment__group__property__in=self.get_allowed_properties()
#         ).select_related(
#             "sub_segment",
#             "sub_segment__segment",
#             "sub_segment__segment__group",
#             "sub_segment__segment__group__property",
#         )

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs["allowed_properties"] = self.get_allowed_properties()
#         return kwargs

#     def get_success_url(self):
#         property_id = self.object.property.id
#         return reverse("mappings:group-list") + f"?property={property_id}"









# # from django.contrib.auth.mixins import LoginRequiredMixin
# # from django.urls import reverse_lazy, reverse
# # from django.views.generic import ListView, CreateView, UpdateView, DeleteView

# # from .forms import SegmentGroupForm, SegmentForm, SubSegmentForm, DetailSegmentForm
# # from .models import SegmentGroup, Segment, SubSegment, DetailSegment
# # from properties.models import UserPropertyAccessMixin


# # class SegmentGroupListView(LoginRequiredMixin, UserPropertyAccessMixin, ListView):
# #     model = SegmentGroup
# #     template_name = "mappings/group_list.html"
# #     context_object_name = "groups"

# #     def get_queryset(self):
# #         property_obj = self.get_selected_property()
# #         return SegmentGroup.objects.filter(property=property_obj).prefetch_related("segments")
    

# # class SegmentGroupCreateView(LoginRequiredMixin, UserPropertyAccessMixin, CreateView):
# #     model = SegmentGroup
# #     form_class = SegmentGroupForm
# #     template_name = "mappings/group_form.html"

# #     def form_valid(self, form):
# #         form.instance.property = self.get_selected_property()
# #         return super().form_valid(form)

# #     def get_success_url(self):
# #         return reverse("mappings:group-list") + f"?property={self.get_selected_property().id}"
    

# # class SegmentGroupUpdateView(LoginRequiredMixin, UserPropertyAccessMixin, UpdateView):
# #     model = SegmentGroup
# #     form_class = SegmentGroupForm
# #     template_name = "mappings/group_form.html"

# #     def get_queryset(self):
# #         return SegmentGroup.objects.filter(property__in=self.get_allowed_properties())

# #     def get_success_url(self):
# #         return reverse("mappings:group-list") + f"?property={self.object.property_id}"
    

# # class SegmentGroupDeleteView(LoginRequiredMixin, UserPropertyAccessMixin, DeleteView):
# #     model = SegmentGroup
# #     template_name = "mappings/group_confirm_delete.html"

# #     def get_queryset(self):
# #         return SegmentGroup.objects.filter(property__in=self.get_allowed_properties())

# #     def get_success_url(self):
# #         return reverse("mappings:group-list") + f"?property={self.object.property_id}"
    

# # class SegmentCreateView(LoginRequiredMixin, UserPropertyAccessMixin, CreateView):
# #     model = Segment
# #     form_class = SegmentForm
# #     template_name = "mappings/segment_form.html"

# #     def get_form_kwargs(self):
# #         kwargs = super().get_form_kwargs()
# #         kwargs["property_obj"] = self.get_selected_property()
# #         return kwargs

# #     def get_success_url(self):
# #         return reverse("mappings:group-list") + f"?property={self.get_selected_property().id}"


# # class SegmentUpdateView(LoginRequiredMixin, UserPropertyAccessMixin, UpdateView):
# #     model = Segment
# #     form_class = SegmentForm
# #     template_name = "mappings/segment_form.html"

# #     def get_queryset(self):
# #         return Segment.objects.filter(group__property__in=self.get_allowed_properties())

# #     def get_form_kwargs(self):
# #         kwargs = super().get_form_kwargs()
# #         kwargs["property_obj"] = self.object.property
# #         return kwargs

# #     def get_success_url(self):
# #         return reverse("mappings:group-list") + f"?property={self.object.property.id}"


# # class SegmentDeleteView(LoginRequiredMixin, UserPropertyAccessMixin, DeleteView):
# #     model = Segment
# #     template_name = "mappings/segment_confirm_delete.html"

# #     def get_queryset(self):
# #         return Segment.objects.filter(group__property__in=self.get_allowed_properties())

# #     def get_success_url(self):
# #         return reverse("mappings:group-list") + f"?property={self.object.property.id}"
    

# # class SubSegmentCreateView(LoginRequiredMixin, UserPropertyAccessMixin, CreateView):
# #     model = SubSegment
# #     form_class = SubSegmentForm
# #     template_name = "mappings/subsegment_form.html"

# #     def get_form_kwargs(self):
# #         kwargs = super().get_form_kwargs()
# #         kwargs["property_obj"] = self.get_selected_property()
# #         return kwargs

# #     def get_success_url(self):
# #         return reverse("mappings:group-list") + f"?property={self.get_selected_property().id}"


# # class SubSegmentUpdateView(LoginRequiredMixin, UserPropertyAccessMixin, UpdateView):
# #     model = SubSegment
# #     form_class = SubSegmentForm
# #     template_name = "mappings/subsegment_form.html"

# #     def get_queryset(self):
# #         return SubSegment.objects.filter(segment__group__property__in=self.get_allowed_properties())

# #     def get_form_kwargs(self):
# #         kwargs = super().get_form_kwargs()
# #         kwargs["property_obj"] = self.object.property
# #         return kwargs

# #     def get_success_url(self):
# #         return reverse("mappings:group-list") + f"?property={self.object.property.id}"


# # class SubSegmentDeleteView(LoginRequiredMixin, UserPropertyAccessMixin, DeleteView):
# #     model = SubSegment
# #     template_name = "mappings/subsegment_confirm_delete.html"

# #     def get_queryset(self):
# #         return SubSegment.objects.filter(segment__group__property__in=self.get_allowed_properties())

# #     def get_success_url(self):
# #         return reverse("mappings:group-list") + f"?property={self.object.property.id}"
    

# # class DetailSegmentCreateView(LoginRequiredMixin, UserPropertyAccessMixin, CreateView):
# #     model = DetailSegment
# #     form_class = DetailSegmentForm
# #     template_name = "mappings/detailsegment_form.html"

# #     def get_form_kwargs(self):
# #         kwargs = super().get_form_kwargs()
# #         kwargs["property_obj"] = self.get_selected_property()
# #         return kwargs

# #     def get_success_url(self):
# #         return reverse("mappings:group-list") + f"?property={self.get_selected_property().id}"


# # class DetailSegmentUpdateView(LoginRequiredMixin, UserPropertyAccessMixin, UpdateView):
# #     model = DetailSegment
# #     form_class = DetailSegmentForm
# #     template_name = "mappings/detailsegment_form.html"

# #     def get_queryset(self):
# #         return DetailSegment.objects.filter(
# #             sub_segment__segment__group__property__in=self.get_allowed_properties()
# #         )

# #     def get_form_kwargs(self):
# #         kwargs = super().get_form_kwargs()
# #         kwargs["property_obj"] = self.object.property
# #         return kwargs

# #     def get_success_url(self):
# #         return reverse("mappings:group-list") + f"?property={self.object.property.id}"


# # class DetailSegmentDeleteView(LoginRequiredMixin, UserPropertyAccessMixin, DeleteView):
# #     model = DetailSegment
# #     template_name = "mappings/detailsegment_confirm_delete.html"

# #     def get_queryset(self):
# #         return DetailSegment.objects.filter(
# #             sub_segment__segment__group__property__in=self.get_allowed_properties()
# #         )

# #     def get_success_url(self):
# #         return reverse("mappings:group-list") + f"?property={self.object.property.id}"
    


# # # def get_queryset(self):
# # #     property_obj = self.get_selected_property()
# # #     return (
# # #         SegmentGroup.objects.filter(property=property_obj)
# # #         .prefetch_related(
# # #             "segments",
# # #             "segments__sub_segments",
# # #             "segments__sub_segments__detail_segments",
# # #         )
# # #     )