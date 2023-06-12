from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny
import uuid


class LoginView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        context = {}
        user = request.user
        print('login view',user)
        try:
            user_object = User.objects.get(username=user)
            if user_object:
                context['status'] = 200
                context['message'] = f'Hello, {user.username}'
                items = item.objects.all()
                item_serializer_obj = item_serializer(items,many=True)
                context['data'] = item_serializer_obj.data
                return Response(context)


        except Exception as e:
            print(e)
            context['status'] = 500
            context['message'] = str(e)
            return Response(context)

class items_list(APIView):
    authentication_classes = []
    permission_classes = []
    
    def get(self,request):
        context = {}
        data = request.data
        if not "category" in data:
            item_objects = item.objects.all()
            item_serializer_object = item_serializer(item_objects,many=True)
            context['status'] = 200
            context['message'] = 'Success'
            context['data'] = item_serializer_object.data
            return Response(context)



        category = data['category']
        try:
            category_object = Category.objects.get(category_name = category)
            if category_object is None:
                context['status'] = 500
                context['message'] = 'category not found'
                context['data'] = ""
                return Response(context)

            item_objects = item.objects.filter(category= category_object)
            if item_objects:
                item_serializer_object = item_serializer(item_objects,many=True)
                context['status'] = 200
                context['message'] = 'Success'
                context['data'] = item_serializer_object.data
            else:
                context['status'] = 500
                context['message'] = 'data not found'
                context['data'] = ""
            return Response(context)


        except Exception as e:
            context['status'] = 500
            context['message'] = str(e)
            context['data'] = ''

        return Response(context)










class add_to_cart(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = (AllowAny,)

    def get(self,request):
        user = request.user
        try:
            user_object = User.objects.get(username=user)
            cart_objects = Cart.objects.filter(user_name = user_object)
            if not cart_objects:
                return Response({'status':200,'message':'Your cart is empty','data':""})
            cart_serializer_object = cart_serializer(cart_objects,many=True)
            return Response({'status':200,'message':'Success','data':cart_serializer_object.data})
        except Exception as e:
            print(e)
            return Response({'status':500,'message': str(e),'data': ""})

    
    def post(self,request):
        user = request.user
        data = request.data
        print(request.user)
        context = {}
        data_found = False
        try:
            item_name = data['item_name']
            item_object = item.objects.get(item_name=item_name)
            item_price = item_object.item_price
            # if  request.user.is_anonymous:
            #     anonymous_user_cart = Cart.objects.create(items=item_object,session_id = uuid.uuid4())
            #     anonymous_user_cart.save()
            #     anonymous_user_cart_serializer_object = cart_object(anonymous_user_cart)
            #     context['status'] = '200'
            #     context['message'] = 'cart created and item added successfully for anonymous user'
            #     context['data'] = anonymous_user_cart_serializer_object.data
            #     return Response(context)


            user_object = User.objects.get(username=user)
            user_cart_object = Cart.objects.filter(user_name=user_object)

            if user_cart_object:
                for cart_object in user_cart_object:
                    if cart_object.items_id == item_object.id:
                        cart_object.quantity = cart_object.quantity + 1
                        cart_object.total_price = cart_object.total_price + item_price
                        cart_object.save()
                        user_cart_serializer_object = cart_serializer(cart_object)
                        data_found = True
                        break
                if not data_found:
                    new_item_to_cart = Cart.objects.create(user_name=user_object,items=item_object)
                    new_item_to_cart.total_price = item_price
                    new_item_to_cart.save()
                    user_cart_serializer_object = cart_serializer(new_item_to_cart)
                        
                


                context['status'] = '200'
                context['message'] = 'cart exists'
                context['data'] = user_cart_serializer_object.data
                
            else:
                new_cart_object = Cart.objects.create(user_name=user_object,items=item_object)
                new_cart_object.save()
                context['status'] = 201
                context['message'] = 'New Cart is Created and item is added successfully'

            return Response(context)

        except Exception as e:
            print(e)
            context['status'] = 500
            context['message'] = str(e)
            return Response(context)

    def delete(self, request):
        user = request.user
        data = request.data
        context = {}
        data_found = False
        try:
            if not "item_name" in data:
                context['status'] = 400
                context['message'] = "BAD_REQUEST"
                context['data'] = ""
                return Response(context)
            item_name = data['item_name']
            user_object = User.objects.get(username=user)
            item_object = item.objects.get(item_name=item_name)
            user_cart_object = Cart.objects.filter(user_name=user_object)
            item_price = item_object.item_price
            if user_cart_object:
                for cart_object in user_cart_object:
                    if cart_object.items_id == item_object.id:
                        data_found = True
                        if int(cart_object.quantity) == 0:
                            cart_object.delete()
                            context['status'] = 404
                            context['message'] = 'Item not found'
                        else:
                            context['status'] = 200
                            context['message'] = 'Item deleted from cart successfully'
                            cart_object.quantity = cart_object.quantity - 1
                            cart_object.total_price = cart_object.total_price - item_price
                            cart_object.save()
                            user_cart_serializer_object = cart_serializer(cart_object)
                            context['data'] = user_cart_serializer_object.data
                        break
                if not data_found:
                    context['status'] = 500
                    context['message'] = 'Item not found'
                    context['data'] = ""
                return Response(context)

            else:
                context['status'] = 404
                context['message'] = 'Internal server error'
                return Response(context)
        except Exception as e:
            context['status'] = 500
            context['message'] = str(e)
            return Response(context)


                    

        
        


        

