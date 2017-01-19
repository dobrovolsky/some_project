from django.contrib import auth, messages
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, RedirectView, CreateView, FormView

from .forms import CommentForm
from .models import Product, Comment


class ProductListView(ListView):
    """
    View with all Products
    """
    template_name = 'product/products.html'
    paginate_by = 5
    context_object_name = 'product_list'

    def get_queryset(self):
        """
        Changed queryset for sorting objects
        """
        sort_mode = self.request.COOKIES.get('sort', '-created_at')
        sorted_products = Product.objects.prefetch_related('user_id').annotate(like_count=Count('user_id')).order_by(
            sort_mode)
        return sorted_products


class ProductDetailView(DetailView):
    """
    View with Product
    """
    template_name = 'product/product.html'
    context_object_name = 'product'
    model = Product

    def get_context_data(self, **kwargs):
        """
        Add comments to context
        """
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.recently_added(product=self.object)
        return context


class CommentView(CreateView):
    """
    handler adding comment
    """
    form_class = CommentForm

    def form_valid(self, form):
        """
        Add message and success_url
        :param form:
        :return:
        """
        self.success_url = reverse('product_slug', args=[form.cleaned_data['product_id'].slug])
        messages.success(self.request, 'Thank you for comment')
        return super(CommentView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'You must fill field')
        return redirect(reverse('product_slug', args=[form.cleaned_data['product_id'].slug]))


class LoginView(FormView):
    """
    handler login
    """
    form_class = AuthenticationForm
    template_name = 'product/login_page.html'

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return redirect('products')

    def form_invalid(self, form):
        messages.error(self.request, 'You made mistake, try again')
        return redirect('login')


class LogoutView(RedirectView):
    """
    handler logout
    """
    url = reverse_lazy('products')

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class LikeView(View):
    """
    handler adding and removing like
    """

    def post(self, request):
        if request.user.is_authenticated():
            product = get_object_or_404(Product, id=request.POST['product_id'])
            # Change like. If like was - delete, if not - add.
            product.change_state_like(request.user.id)
            messages.success(request, 'Like changed')
        else:
            # If user doesn't authenticate show the messages error.
            messages.error(request, 'You have to sing in for doing this action')
        # Refresh page.
        return redirect(reverse('product_slug', args=[request.POST['slug']]))
