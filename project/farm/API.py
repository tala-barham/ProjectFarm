from django.http import JsonResponse
from .models import Location,Farm,Farmer,Resource,Animal,AnimalType
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

#display functions
def location_api(request):
    locations = Location.objects.values()
    data = list(locations)
    return JsonResponse({'locations': data})

def farm_api(request):
    farms = Farm.objects.values('id', 'name', 'size', 'location__name')
    data = list(farms)
    return JsonResponse({'farms': data})

def farmer_api(request):
    farmers = Farmer.objects.values()
    data = list(farmers)
    return JsonResponse({'farmers': data})

def resource_api(request):
    resources = Resource.objects.values('id', 'name', 'quantity', 'expiration_date', 'farm_resource__name')
    data = list( resources)
    return JsonResponse({'resources': data})

def animal_type_api(request):
    animal_types = AnimalType.objects.values()
    data = list(animal_types)
    return JsonResponse({'animal_types': data})

def animal_api(request):
    animals = Animal.objects.select_related('animal_type').prefetch_related('resources').values('id', 'gender', 'health_status', 'animal_type__name', 'resources__name')
    data = list(animals)
    return JsonResponse({'animals': data})

#add functions
@csrf_exempt    
def add_location_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            if name:
                location = Location(name=name)
                location.save()
                return JsonResponse({'message': 'Location added successfully'})
            else:
                return JsonResponse({'message': 'Name is required'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405) 
    
@csrf_exempt
def add_farm_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            size = data.get('size')
            location_id = data.get('location_id')  
            if name and size and location_id:
                location = Location.objects.get(pk=location_id)  
                farm = Farm(name=name, size=size, location=location)
                farm.save()
                return JsonResponse({'message': 'Farm added successfully'})
            else:
                return JsonResponse({'message': 'Name, size, and location are required'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
    
@csrf_exempt  
def add_farmer_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            if name:
                farmer = Farmer(name=name)
                farmer.save()
                return JsonResponse({'message': 'Farmer added successfully'})
            else:
                return JsonResponse({'message': 'Name is required'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
    
@csrf_exempt
def add_resource_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            quantity = data.get('quantity')
            expiration_date = data.get('expiration_date')
            farm_ids = data.get('farm_resource')

            if name and quantity and expiration_date:
                # Create the resource object
                resource = Resource(name=name, quantity=quantity, expiration_date=expiration_date)
                resource.save()

                if farm_ids:
                    farms = Farm.objects.filter(pk__in=farm_ids)
                    resource.farm_resource.set(farms)

                return JsonResponse({'message': 'Resource added successfully'})
            else:
                return JsonResponse({'message': 'Name, quantity, and expiration_date are required'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def add_animal_type_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            if name:
                animal_type = AnimalType(name=name)
                animal_type.save()
                return JsonResponse({'message': 'AnimalType added successfully'})
            else:
                return JsonResponse({'message': 'Name is required'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt    
def add_animal_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            gender = data.get('gender')
            health_status = data.get('health_status')
            animal_type_id = data.get('animal_type')
            resource_ids = data.get('resources')
            
            if gender and health_status and animal_type_id:
                animal_type = AnimalType.objects.get(pk=animal_type_id)
                animal = Animal(gender=gender, health_status=health_status, animal_type=animal_type)
                animal.save()
                
                if resource_ids:
                    resources = Resource.objects.filter(pk__in=resource_ids)
                    animal.resources.set(resources)
                return JsonResponse({'message': 'Animal added successfully'})
            else:
                return JsonResponse({'message': 'Gender, health_status, and animal_type are required'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
    
###delete functions
@csrf_exempt 
def delete_location_api(request, location_id):
    if request.method == 'DELETE':
        location = get_object_or_404(Location, pk=location_id)
        location.delete()
        return JsonResponse({'message': 'Location deleted successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
    
@csrf_exempt 
def delete_farm_api(request, farm_id):
    if request.method == 'DELETE':
        farm = get_object_or_404(Farm, pk=farm_id)
        farm.delete()
        return JsonResponse({'message': 'Farm deleted successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
    
@csrf_exempt     
def delete_farmer_api(request, farmer_id):
    if request.method == 'DELETE':
        farmer = get_object_or_404(Farmer, pk=farmer_id)
        farmer.delete()
        return JsonResponse({'message': 'Farmer deleted successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt        
def delete_resource_api(request, resource_id):
    if request.method == 'DELETE':
        resource = get_object_or_404(Resource, pk=resource_id)
        resource.delete()
        return JsonResponse({'message': 'Resource deleted successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405) 

@csrf_exempt     
def delete_animal_type_api(request, animal_type_id):
    if request.method == 'DELETE':
        animal_type = get_object_or_404(AnimalType, pk=animal_type_id)
        animal_type.delete()
        return JsonResponse({'message': 'Animal type deleted successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)     
    
@csrf_exempt  
def delete_animal_api(request, animal_id):
    if request.method == 'DELETE':
        animal = get_object_or_404(Animal, pk=animal_id)
        animal.delete()
        return JsonResponse({'message': 'Animal deleted successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)   
    
######edit functions
@csrf_exempt 
def edit_farm_api(request, farm_id):
    if request.method == 'PUT':
        farm = get_object_or_404(Farm, pk=farm_id)

        try:
            data = json.loads(request.body)
            farm_name = data.get('name')
            farm_size = data.get('size')
            location_id = data.get('location')  # Assuming the location ID is provided

            if farm_name:
                farm.name = farm_name

            if farm_size:
                farm.size = farm_size

            if location_id:
                location = get_object_or_404(Location, pk=location_id)
                farm.location = location

            farm.save()
            return JsonResponse({'message': 'Farm edited successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
    
@csrf_exempt    
def edit_farmer_api(request, farmer_id):
    if request.method == 'PUT':
        farmer = get_object_or_404(Farmer, pk=farmer_id)

        try:
            data = json.loads(request.body)
            farmer_name = data.get('name')

            if farmer_name:
                farmer.name = farmer_name

            farmer.save()
            return JsonResponse({'message': 'Farmer edited successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)    
    
@csrf_exempt    
def edit_resource_api(request, resource_id):
    if request.method == 'PUT':
        resource = get_object_or_404(Resource, pk=resource_id)

        try:
            data = json.loads(request.body)
            resource_name = data.get('name')
            resource_quantity = data.get('quantity')
            resource_expiration_date = data.get('expiration_date')
            farm_ids = data.get('farm_resource')

            if resource_name:
                resource.name = resource_name

            if resource_quantity:
                resource.quantity = resource_quantity

            if resource_expiration_date:
                resource.expiration_date = resource_expiration_date

            resource.save()

            if farm_ids:
                farms = Farm.objects.filter(pk__in=farm_ids)
                resource.farm_resource.set(farms)

            return JsonResponse({'message': 'Resource edited successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
    
@csrf_exempt 
def edit_animal_type_api(request, animal_type_id):
    if request.method == 'PUT':
        animal_type = get_object_or_404(AnimalType, pk=animal_type_id)

        try:
            data = json.loads(request.body)
            animal_type_name = data.get('name')

            if animal_type_name:
                animal_type.name = animal_type_name

            animal_type.save()
            return JsonResponse({'message': 'Animal type edited successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)  
    
@csrf_exempt 
def edit_animal_api(request, animal_id):
    if request.method == 'PUT':
        animal = get_object_or_404(Animal, pk=animal_id)

        try:
            data = json.loads(request.body)
            gender = data.get('gender')
            health_status = data.get('health_status')
            animal_type_id = data.get('animal_type')
            resource_ids = data.get('resources')

            if gender:
                animal.gender = gender

            if health_status:
                animal.health_status = health_status

            if animal_type_id:
                animal.animal_type_id = animal_type_id

            animal.save()

            if resource_ids:
                resources = Resource.objects.filter(pk__in=resource_ids)
                animal.resources.set(resources)

            return JsonResponse({'message': 'Animal edited successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405) 