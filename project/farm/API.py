from django.http import JsonResponse
from .models import Location,Farm,Farmer,Resource,Animal,AnimalType
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

class CRUDMixin:
    def __init__(self, model):
        self.model = model
        
    def list_objects(self, request, fields=None):
        if request.method == 'GET':
            if fields:
                objects = self.model.objects.values(*fields)
            else:
                try:
                    objects = self.model.objects.values()
                except TypeError:
                    return JsonResponse({'message': 'Invalid model'}, status=400)
            data = list(objects)
            return JsonResponse({f'{self.model.__name__.lower()}s': data})
        else:
            return JsonResponse({'message': 'Invalid request method'}, status=405)
        
    @csrf_exempt
    def create_object(self, request):
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                required_fields = getattr(self, 'required_fields', [])
                many_to_many_field = getattr(self, 'many_to_many_field', None)
                if all(field in data for field in required_fields):
                    obj = self.model(**{field: data[field] for field in required_fields})
                    obj.save()
                    if many_to_many_field:
                        related_ids = data.get(many_to_many_field)
                        if related_ids:
                            related_objects = self.model._meta.get_field(many_to_many_field).related_model.objects.filter(pk__in=related_ids)
                            getattr(obj, many_to_many_field).set(related_objects)
                    return JsonResponse({'message': f'{self.model.__name__} added successfully'})
                else:
                    return JsonResponse({'message': f'Required fields: {", ".join(required_fields)}'}, status=400)
            except json.JSONDecodeError:
                return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        else:
            return JsonResponse({'message': 'Invalid request method'}, status=405)

    @csrf_exempt
    def edit_object(self, request, instance_id):
        if request.method == 'PUT':
            obj = get_object_or_404(self.model, pk=instance_id)
            try:
                data = json.loads(request.body)
                for field, value in data.items():
                    setattr(obj, field, value)
                    obj.save()
                    return JsonResponse({'message': f'{self.model.__name__} edited successfully'})
            except json.JSONDecodeError:
                return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        else:
            return JsonResponse({'message': 'Invalid request method'}, status=405)
    
    @csrf_exempt
    def delete_object(self, request, instance_id): 
        if request.method == 'DELETE':
            obj = get_object_or_404(self.model, pk=instance_id)
            obj.delete()
            return JsonResponse({'message': f'{self.model.__name__} deleted successfully'})
        else:
            return JsonResponse({'message': 'Invalid request method'}, status=405)

class LocationApi(CRUDMixin):
    required_fields = ['name']
    
    def __init__(self):
        super().__init__(Location)    

class FarmApi(CRUDMixin):
    required_fields = ['name', 'size', 'location_id']
    
    def __init__(self):
        super().__init__(Farm)

class FarmerApi(CRUDMixin):
    required_fields = ['name']
    
    def __init__(self):
        super().__init__(Farmer)
        
class ResourceApi(CRUDMixin):
    required_fields = ['name', 'quantity', 'expiration_date'] 
    many_to_many_field = 'farm_resource'
    
    def __init__(self):
        super().__init__(Resource)
        
class AnimalTypeApi(CRUDMixin):
    required_fields = ['name'] 
    
    def __init__(self):
        super().__init__(AnimalType)
        
class AnimalApi(CRUDMixin):
    required_fields = ['gender', 'health_status', 'animal_type_id'] 
    many_to_many_field = 'resources'
    
    def __init__(self):
        super().__init__(Animal)     