from django.forms import DateInput
from django_filters import FilterSet, ModelChoiceFilter, DateFilter
from .models import Post, Category


# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django джене рики.

class PostFilter(FilterSet):
    category =ModelChoiceFilter(
        field_name='postcategory__category', # требуется, для того чтобы сделать свою фильтрации с изменением названия
        queryset=Category.objects.all(),
        label='Тэги',
        empty_label='любая'
    )

    TimeAdding = DateFilter(
        'date_post',
        lookup_expr='gt',
        label='Дата не раньше',
        widget=DateInput(
            attrs={
                'type': 'date'
            }
        )
    )

    class Meta:
# В Meta классе мы должны указать Django модель,
# в которой будем фильтровать записи.
        model = Post
# В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
        fields = {
            'header_post': ['icontains'],
        }
