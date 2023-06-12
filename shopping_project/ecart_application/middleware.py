# from rest_framework.permissions import IsAuthenticated
# from re import sub
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.authtoken.models import Token

# class CustomMiddleware(object):

#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):


#         print(request.user)
#         response = self.get_response(request)
#         return response

#     def process_view(self, request, view_func, view_args, view_kwargs):
#         print(request)
#         header_token = request.META.get('HTTP_AUTHORIZATION', None)
#         if header_token is not None:
#             try:
#                 token = sub('Token ', '', header_token)
#                 token_obj = Token.objects.get(key = token)
#                 request.user = token_obj.user
#             except Exception as e:
#                 pass
#         print(request.user)
#         return None

#     def process_exception(self, request, exception):
#         """
#         Called when a view raises an exception.
#         """
#         return None

#     def process_template_response(self, request, response):
#         """
#         Called just after the view has finished executing.
#         """
#         return response