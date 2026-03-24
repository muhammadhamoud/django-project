call "C:\Users\muhammad.hamoud\Desktop\ng\backend\venv\scripts\activate"

@REM call python manage.py loaddata permission_groups.json
@REM call python manage.py loaddata permissions.json
@REM call python manage.py loaddata role_templates.json
@REM call python manage.py loaddata roles.json
@REM call python manage.py loaddata properties.json
@REM python manage.py loaddata report_groups.json
@REM python manage.py loaddata reports.json

python manage.py tailwind start

python manage.py makemigrations & python manage.py migrate
python manage.py showmigrations
@REM fix migrations
python manage.py migrate settings zero --fake
python manage.py migrate settings


python manage.py shell -c "from reports.models import Report, ReportGroup; Report.objects.all().delete(); ReportGroup.objects.all().delete()"



call conda activate dj
call cd backend\site & python manage.py makemigrations & python manage.py migrate 
call python manage.py createsuperuser --email=admin@admin.com
call python manage.py runserver

call stripe listen --forward-to http://127.0.0.1:8000/webhook/

python -Xutf8 manage.py dumpdata homepage > homepage_data.json
python -Xutf8 manage.py dumpdata shop > shop_data.json
python manage.py loaddata homepage_data.json

python -Xutf8 manage.py dumpdata addresses.addresstype > addresstype.json

call python manage.py homepage --generate
call python manage.py blogs --generate

call python manage.py categories --generate --models Tag Attribute Category
call python manage.py products --generate --models ProductLabel Product
@REM call ProductImage
call python manage.py addresses --generate

@REM call python manage.py fake_homepage_translated --flush 

@REM call python manage.py startapp account
@REM call python manage.py startapp location
@REM call python manage.py startapp rental
@REM call python manage.py startapp coupon
@REM call python manage.py startapp payment
@REM call python manage.py startapp feedback
@REM call python manage.py startapp booking
@REM call python manage.py startapp invoice
@REM call python manage.py startapp maintenance
@REM call python manage.py startapp notification
@REM call python manage.py startapp configuration
@REM call python manage.py startapp faq
@REM call python manage.py startapp dashboard
@REM call python manage.py startapp detail
@REM call python manage.py startapp management
@REM call python manage.py startapp transaction
@REM call python manage.py startapp car


@REM call mkdir "./apps/ecommerce/product"
@REM call mkdir "./apps/ecommerce/user_profile"
@REM call mkdir "./apps/ecommerce/order"
@REM call mkdir "./apps/ecommerce/payment"
@REM call mkdir "./apps/ecommerce/cart"
@REM call mkdir "./apps/ecommerce/checkout"
@REM call mkdir "./apps/ecommerce/chat"
@REM call mkdir "./apps/ecommerce/core"

@REM call python manage.py startapp product ./apps/ecommerce/product 
@REM call python manage.py startapp user_profile ./apps/ecommerce/user_profile
@REM call python manage.py startapp order ./apps/ecommerce/order 
@REM call python manage.py startapp payment ./apps/ecommerce/payment
@REM call python manage.py startapp cart ./apps/ecommerce/cart
@REM call python manage.py startapp checkout ./apps/ecommerce/checkout
@REM call python manage.py startapp chat ./apps/ecommerce/chat
@REM call python manage.py startapp core ./apps/ecommerce/core


@REM call python manage.py loaddata carrental/ratemanagement/ratepool.json
@REM call python manage.py loaddata carrental/ratemanagement/ratetype.json
@REM call python manage.py loaddata carrental/ratemanagement/ratecategory.json
@REM call python manage.py loaddata carrental/ratemanagement/ratesegment.json
@REM call python manage.py loaddata carrental/ratemanagement/ratesegmentgroup.json
@REM call python manage.py loaddata carrental/ratemanagement/ratecode.json
@REM call python manage.py loaddata carrental/ratemanagement/ratecodecluster.json
@REM call python manage.py loaddata carrental/ratemanagement/rateoffer.json
@REM call python manage.py loaddata carrental/ratemanagement/rateofferproduct.json
@REM call python manage.py loaddata carrental/ratemanagement/rateruletype.json
@REM call python manage.py loaddata carrental/ratemanagement/dayoftheweek.json

@REM call python manage.py loaddata homepage/site_information_fixture.json



echo "# django-project" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/muhammadhamoud/django-project.git
git push -u origin main