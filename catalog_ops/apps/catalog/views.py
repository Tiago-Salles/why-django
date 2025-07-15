import datetime
import json
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from django.db.models import F, Func
from django.db.models.functions import MD5
from rest_framework.response import Response
from decimal import Decimal
from django.http import JsonResponse


service_config = {
    "service_name": "portugal_digital",
    "endpoint_url": "https://academiaportugaldigital.pt/api/api/Course/FinishedIntegrationNau",
    "auth_token": "XXXXXXXXXXXXXXXXXXXXX",
    "auth_type": "bearer",
    "auth_header": "Authorization",
    "page_size": 100,
    "days": 30,
    "fields": [
        {
        "name": "name",
        "func": "nau_openedx_extensions.coursecertificate.extractors.student_email",
        "trans": "md5",  
        },
        {
        "name": "price",
        "func": "nau_openedx_extensions.coursecertificate.extractors.course_id"      
        },
        {
        "name": "description",
        "func": "nau_openedx_extensions.coursecertificate.extractors.course_id",
        "trans": "Md5",      
        }
    ],    
    "filters": [
        {
        "func": "nau_openedx_extensions.coursecertificate.filters.certificate_by_course_id_regex",
        "args": "course-v1"
        },
        {
        "func": "nau_openedx_extensions.coursecertificate.filters.certificate_by_org",
        "args": "EduNext"
        }
    ]
}

def get_certificates_queryset(transformations: dict, service_fields: list = []):
    """Get certificates queryset filtered by date"""
    query = Product.objects.all()
    if transformations:
        transformed_fields: list = []
        annotations = {}
        
        for original_name, trans_config in transformations.items():
            transformed_fields.append(trans_config["encrypted_field_name"])
            annotations[trans_config["encrypted_field_name"]] = trans_config["encryption_method"]
            service_fields.remove(original_name)
        
        fields = [*service_fields, *transformed_fields]

        return query.annotate(**annotations).values(*fields)
    
    return query.values(*service_fields)

def check_fields_to_encrypt(service_config: dict):
    """
    NAU_SEND_COURSE_CERTIFICATE_CONFIG:
    - service_name: portugal_digital
        endpoint_url: https://academiaportugaldigital.pt/api/api/Course/FinishedIntegrationNau
        auth_token: XXXXXXXXXXXXXXXXXXXXX
        auth_type: bearer
        auth_header: Authorization
        page_size: 100
        days: 30
        fields:
        - name: name
            func: nau_openedx_extensions.coursecertificate.extractors.student_email
            trans: md5
        - name: value
            func: nau_openedx_extensions.coursecertificate.extractors.course_id
    
    the return
    
    {
        "name": {
            "encrypted_field_name": "name_MD5",
            "encryption_method": MD5(F(name))
        }
    }
    
    or 
        
    {
        "name": {
            "encrypted_field_name": "name_BASE64",
            "encryption_method": ToBase64(F(name))
        }
    }
    """

    fields = service_config.get("fields")
    annotations = {}
    
    for field in fields:
        trans = field.get("trans")
        
        if trans:
            
            # We don't use `get` method here
            # because a not valid encryption
            # must fail the service
            try:
                trans_as_upper = trans.upper()
                encryption_method = {
                    "MD5": MD5(F(field["name"])),
                    "BASE64": ToBase64(F(field["name"]))
                }[trans_as_upper]
                encryption_field = f"{field['name']}_{trans_as_upper}"
                annotations[field['name']] = {
                    "encrypted_field_name": encryption_field,
                    "encryption_method": encryption_method
                }
            except Exception as e:
                raise e

    return annotations

class ProductViewSet(viewsets.ViewSet):
    
    def list(self, request):
        data = build_response()
        return Response(data)
    
class ToBase64(Func):
    function = 'TO_BASE64'

def build_response():
    ...
    service_fields = service_config.get("fields")
    service_fields = [f["name"] for f in service_fields]
    transformations = check_fields_to_encrypt(service_config)
    query = get_certificates_queryset(transformations, service_fields)
    ...
    return list(query)
  
# def build_response():
#     products = Product.objects.annotate(
#         **{
#             "name": MD5(F('name')),
#             "name_base64": ToBase64(F('name'))
#         }
#     ).values(
#         'uuid', 'name_md5', 'name_base64', 'price', 'is_active', 'quantity', 'description',
#     )
#     
#     data = [
#         {
#             'uuid': p['uuid'],
#             'name': p['name_md5'],
#             'name_2': p['name_base64'],
#             'price': Decimal(p['price']),
#             'is_active': p['is_active'],
#             'quantity': p['quantity'],
#             'description': p['description'],
#         }
#         for p in products
#     ]
#     
#     return data




