# runa

python manage.py runserver

from runa.models import Category
from runa.serializers import CategorySerializer
s = CategorySerializer()
print(repr(s))

docker-compose exec web python manage.py shell
docker-compose exec web python manage.py load

docker-compose exec web python manage.py test
