from haversine import haversine

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q, F, Min

from products.models import Product

class ProductsView(View):
    def get(self, request):
        sort_key = request.GET.get('sort_key','low_price')
        region   = request.GET.get('region')
        themes   = request.GET.getlist('themes')
        offset   = int(request.GET.get('offset', 0))
        limit    = int(request.GET.get('limit', 30))
        
        # if region:
            # return JsonResponse({'message' : 'There Is No Region'})

        q = Q()

        for theme in themes:
            q &= Q(ammenity__name = theme)            
        
        p = Q()
        
        if region:
            p = Q(region__name = region)
        
        sort_set = {
            'random' : '?',
            'low_price' : 'price',
            'high_price' : '-price'
        }
        
        ia = (33.431441,126.874237)

        products = Product.objects.filter(p).filter(q).annotate(
            price = Min('room__price')
        ).order_by(sort_set.get(sort_key))[offset:offset + limit]
        result = [
            {
                'id'         : product.id,
                'name'       : product.name,
                'address'    : product.address,
                'price'      : int(product.price),
                'latitude'   : product.latitude,
                'longtitude' : product.longtitude,
                'distance'   : haversine(ia, (product.latitude,product.longtitude), unit = 'm'),
                'region'     : product.region.name,
                'themes'     : [
                   theme.name for theme in product.theme.all()
                ],
                'image'      : product.productimage_set.filter(is_main = True).first().url
            }for product in products
        ]

        return JsonResponse({'products' : result}, status = 200) 