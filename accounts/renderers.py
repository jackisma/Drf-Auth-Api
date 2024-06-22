from rest_framework import renderers 
import json 

# Defining a class to have custom json response 
class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if 'ErrorDetail' in str(data):
            response = json.dumps({"errors" : data})
        else:
            response = json.dumps(data)     

        return response        