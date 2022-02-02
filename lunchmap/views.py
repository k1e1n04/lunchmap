from urllib import request
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from .models import Category, Shop, Review
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ShopForm,ReviewForm, SearchForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db.models import Avg

class IndexView(generic.ListView):
    def get_queryset(self):
        q_word = self.request.GET.get('query')

        if q_word:
            object_list = Shop.objects.filter(
                Q(name__icontains=q_word) | Q(favorite_menu__icontains=q_word)| Q(in_camp__icontains=q_word))
        else:
            object_list = Shop.objects.all()
        return object_list


class DetailView(generic.DetailView):
    model = Shop

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(shop_id=context['shop'].pk)
        if len(context['reviews']) != 0:
          avg_rate = context['reviews'].aggregate(Avg("score"))
          context['avg_rate'] = round(avg_rate['score__avg'])
          avg_speed = context['reviews'].aggregate(Avg("speed"))
          context['avg_speed'] = round(avg_speed['speed__avg'])
        if Review.objects.filter(user_id=self.request.user.pk,shop_id=context['shop'].pk).exists():
          return context
        else:
          context['review_form'] = ReviewForm(
            initial={
              'shop': context['shop'],
            }
          )
          return context

class CreateView(generic.edit.CreateView):
    model = Shop
    fields = ['name', 'address', 'category','favorite_menu','length','in_camp'] # '__all__'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)

class UpdateView(LoginRequiredMixin,generic.edit.UpdateView):
    model = Shop
    fields = '__all__'

class DeleteView(LoginRequiredMixin,generic.edit.DeleteView):
    model = Shop
    success_url = reverse_lazy('lunchmap:index')

def review_create(request):
  if request.method == 'POST':
        reviewForm = ReviewForm(request.POST)
        if reviewForm.is_valid():
            review = reviewForm.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('lunchmap:detail',review.shop.id)

def review_delete(request, id):
  review = get_object_or_404(Review, pk=id)
  review_shop = review.shop
  review.delete()

  context = {
      'message': 'Delete review ' + str(id),
  }
  return redirect('lunchmap:detail',review_shop.id)