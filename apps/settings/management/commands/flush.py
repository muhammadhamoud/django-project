from properties.models import Property
from settings.models import SegmentGroup, SegmentCategory, Segment, SegmentDetail

property_code = "DEMO-RESORT-001"
property_obj = Property.objects.get(resort_code=property_code)

# Optional: delete segment details for that property
SegmentDetail.objects.filter(property=property_obj).delete()

# Delete segments for that property
Segment.objects.filter(category__group__property=property_obj).delete()

# Delete categories for that property
SegmentCategory.objects.filter(group__property=property_obj).delete()

# Delete groups for that property
SegmentGroup.objects.filter(property=property_obj).delete()


from properties.models import Property
from settings.models import SegmentGroup, SegmentCategory, Segment, SegmentDetail

property_code = "DEMO-RESORT-001"
property_obj = Property.objects.get(resort_code=property_code)

SegmentDetail.objects.filter(property=property_obj).delete()
Segment.objects.filter(property=property_obj).delete()
SegmentCategory.objects.filter(property=property_obj).delete()
SegmentGroup.objects.filter(property=property_obj).delete()


python manage.py shell -c "from properties.models import Property; from settings.models import SegmentGroup, SegmentCategory, Segment, SegmentDetail; p=Property.objects.get(resort_code='DEMO-RESORT-001'); SegmentDetail.objects.filter(property=p).delete(); Segment.objects.filter(category__group__property=p).delete(); SegmentCategory.objects.filter(group__property=p).delete(); SegmentGroup.objects.filter(property=p).delete(); print('done')"