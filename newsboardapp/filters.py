from django_filters import FilterSet,DateFromToRangeFilter
from .models import Post
from django_filters.widgets import RangeWidget

class NewsFilter(FilterSet):

   datetime = DateFromToRangeFilter(widget = RangeWidget(attrs={'placeholder': 'YYYY/MM/DD'}))


   class Meta:
       model = Post
       fields = {
           # поиск по названию
           'caption' : ['icontains'],
           'author'  : ['exact'],
       }