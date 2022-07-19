from users.models import User
import django_filters
from django_filters import CharFilter
from django import forms


class UserFilter(django_filters.FilterSet):
    username = CharFilter(field_name="username", lookup_expr='icontains',label='',
                         widget=forms.TextInput(attrs={'class': 'search-box','placeholder': 'Search for a User...'}))

    # price = CharFilter(field_name="price", lookup_expr='lte', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta: 
        model = User
        fields = ['username']