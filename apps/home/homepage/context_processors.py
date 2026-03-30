from .models import SiteInformation, SiteMetaData, SiteInformationAdditional

def site_information(request):
    try:
        site_info = SiteInformation.objects.first()
    except SiteInformation.DoesNotExist:
        site_info = None

    try:
        site_metadata = SiteMetaData.objects.first()
    except SiteMetaData.DoesNotExist:
        site_metadata = None

    try:
        site_info_additional = SiteInformationAdditional.objects.first()
    except SiteInformationAdditional.DoesNotExist:
        site_info_additional = None

    site_data = {
        'site_information': site_info,
        'site_metadata': site_metadata,
        'site_information_additional': site_info_additional,
    }

    # print(site_data)

    return site_data



# def site_information(request):
#     # Retrieve the SiteInformation object (adjust the logic as needed)
#     try:
#         site_info = SiteInformation.objects.all().first()
#     except SiteInformation.DoesNotExist:
#         site_info = None

#     return {'site_information': site_info}
