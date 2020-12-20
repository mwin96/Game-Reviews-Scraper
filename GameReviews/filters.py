import django_filters as df
from .models import Reviews

class ReviewsFilter(df.FilterSet):
    # site = df.ChoiceFilter(field_name = 'website', choices = FILTER_CHOICES)

    site = df.CharFilter(field_name = 'website',lookup_expr= 'icontains', label = 'Review Website:')
    title = df.CharFilter(lookup_expr = 'icontains', label = 'Title:')
    score = df.RangeFilter(label = 'Score:')

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
            super(ReviewsFilter, self).__init__(data=data, queryset=queryset, request=request, prefix=prefix)
            self.filters['score'].field.widget.attrs.update({'class': 'score-range'})
            self.filters['site'].field.widget.attrs.update({'class': 'review-input'})
            self.filters['title'].field.widget.attrs.update({'class': 'title-input'})
    class Meta:
        model = Reviews
        fields = ['site','score']