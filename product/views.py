from django.contrib import auth
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView

from product.models import Product, Comment


class ProductListView(ListView):
    """
    View with all Products
    """
    template_name = 'product/products.html'
    paginate_by = 5
    context_object_name = 'object_list'

    def get_queryset(self):
        """
        Changed queryset for sorting objects
        """
        sort_mode = self.request.COOKIES.get('sort', '-created_at')
        sorted_products = Product.objects.all().order_by(sort_mode)
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
        context['comments'] = Comment.objects.recently_added(product=context[self.context_object_name])
        return context


class CommentView(View):
    """
    handler adding comment
    """

    def post(self, request, **kwargs):
        # Get text from form.
        form_text = request.POST.get('text', '')
        if form_text != '':
            product = get_object_or_404(Product, slug=kwargs['slug'])
            # Create new Comment object.
            Comment.objects.add_comment(comment_text=form_text, product=product)
            messages.success(request, 'Thank you for comment')
        else:
            # If text is show message that fill is empty.
            messages.error(request, 'You must fill field')
        # Refresh page
        return redirect(reverse('product_slug', args=[kwargs['slug']]))


class LoginView(View):
    """
    handler login
    """

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # Return user if it is exist.
        user = auth.authenticate(username=username, password=password)
        # If user exist login user and redirect to 'products' page.
        if request.user.is_authenticated:
            return redirect('products')
        if user is not None:
            auth.login(request, user)
            return redirect('products')
        # If user doesn't exist show message error and reload page.
        messages.error(request, 'You made mistake, try again')
        return self.get(request)

    def get(self, request):
        return render(request, 'product/login_page.html')


class LogoutView(View):
    """
    handler logout
    """

    def get(self, request):
        auth.logout(request)
        return redirect('products')


class LikeView(View):
    """
    handler adding and removing like
    """

    def get(self, request, **kwargs):
        if request.user.is_authenticated():
            product = get_object_or_404(Product, slug=kwargs['slug'])
            # Change like. If like was - delete, if not - add.
            product.change_state_like(request.user.id)
            messages.success(request, 'Like changed')
        else:
            # If user doesn't authenticate show the messages error.
            messages.error(request, 'You have to sing in for doing this action')
        # Refresh page.
        return redirect(reverse('product_slug', args=[kwargs['slug']]))
