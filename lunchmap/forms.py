from django import forms
from .models import Shop, Category, Review #new
 
# new
class ReviewForm(forms.ModelForm):
 
    class Meta:
        model = Review
        fields = ('score','title','review', 'shop','speed')

class SearchForm(forms.Form):
        keyword = forms.CharField(label='検索', max_length=100)

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('name', 'address', 'category','favorite_menu','length','in_camp',)