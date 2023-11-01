from django.http import JsonResponse
from .models import Location,Farm,Farmer,Resource,Animal,AnimalType
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

#display functions
def location_api(request):
    # Retrieve data from the Location model
    locations = Location.objects.values('name')
    # Serialize the data to JSON
    data = list(locations)
    # Return the JSON response
    return JsonResponse(data, safe=False)

def farm_api(request):
    # Retrieve data from the Farm model
    farms = Farm.objects.all()
    # Serialize the data to a JSON-serializable format
    farm_data = []
    for farm in farms:
        farm_data.append({
            'name': farm.name,
            'size': str(farm.size),  # Convert to string to ensure JSON serializability
            'location': farm.location.name  # Assuming 'location' has a 'name' field
        })
    # Return the JSON response
    return JsonResponse(farm_data, safe=False)

def farmer_api(request):
    # Retrieve data from the Location model
    farmers = Farmer.objects.values('name')
    # Serialize the data to JSON
    data = list(farmers)
    # Return the JSON response
    return JsonResponse(data, safe=False)

def resource_api(request):
    # Retrieve data from the Resource model
    resources = Resource.objects.all()
    # Serialize the data to a JSON-serializable format
    resource_data = []
    for resource in resources:
        resource_data.append({
            'name': resource.name,
            'quantity': resource.quantity,
            'expiration_date': resource.expiration_date.strftime('%Y-%m-%d'),
            'farm': [farm.name for farm in resource.farm_resource.all()]  # Assuming 'Farm' has a 'name' field
        })
    # Return the JSON response
    return JsonResponse(resource_data, safe=False)

def animal_type_api(request):
    # Retrieve data from the AnimalType model
    animal_types = AnimalType.objects.values('name')
    # Serialize the data to a JSON-serializable format
    animal_type_data = list(animal_types)
    # Return the JSON response
    return JsonResponse(animal_type_data, safe=False)

def animal_api(request):
    # Retrieve data from the Animal model
    animals = Animal.objects.all()
    # Serialize the data to a JSON-serializable format
    animal_data = []
    for animal in animals:
        animal_data.append({
            'gender': animal.gender,
            'health_status': animal.health_status,
            'animal_type': animal.animal_type.name,
            'resources': [resource.name for resource in animal.resources.all()],
        })
    # Return the JSON response
    return JsonResponse(animal_data, safe=False)

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
            location_id = data.get('location_id')  # Assuming you pass the location ID
            if name and size and location_id:
                location = Location.objects.get(pk=location_id)  # Retrieve the Location object
                farm = Farm(name=name, size=size, location=location)
                farm.save()
                return JsonResponse({'message': 'Farm added successfully'})
            else:
                return JsonResponse({'message': 'Name, size, and location are required'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
    
@csrf_exempt  # You can use @csrf_exempt to temporarily disable CSRF protection for testing (not recommended for production)
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