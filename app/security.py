# from functools import wraps
# # from vardata import *
# from flask import request

# def check_auth(username, password):
#     return username == ruser and password == rpassword

# def login_required(f):
#     @wraps(f)
#     def wrapped_view(**kwargs):
#         auth = request.authorization
#         if not (auth and check_auth(auth.username, auth.password)):
#             return ('Unauthorized', 401, {
#                 'WWW-Authenticate': 'Basic realm="Login Required"'
#             })

#         return f(**kwargs)

#     return wrapped_view


