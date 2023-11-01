from django.shortcuts import get_object_or_404, render,redirect
from.models import Farm,Farmer,Animal,AnimalType,Resource,Location

# Create your views here.

#display functions
def index(request):
    return render(request, 'index.html')

def farm(request):
    farms = Farm.objects.all()
    return render(request, 'farm/farm.html', {'farms': farms})

def farmer(request):
    farmers = Farmer.objects.all()
    return render(request, 'farmer/farmer.html', {'farmers': farmers})

def animal(request):
    animals=Animal.objects.all()
    return render(request, 'animal/animal.html',{'animals':animals})

def location(request):
    locations=Location.objects.all()
    return render(request,'location/location.html', {'locations':locations})

def type_animal(request):
    animal_types = AnimalType.objects.all()
    return render(request, 'animal_type/animal_type.html',{'animal_types':animal_types})

def resource(request):
    resources=Resource.objects.all() 
    return render(request, 'resource/resource.html',{'resources':resources})

#add functions
def add_object(request, model, data, redirect_name):
    if request.method == 'POST':
        model.objects.create(**data)
        return redirect(redirect_name)
    
def add_item(request, model, template_name, redirect_name, fields):
    if request.method == 'POST':
        data = {field: request.POST.get(field) for field in fields}
        model.objects.create(**data)
        return redirect(redirect_name)
    return render(request, template_name)    
    
def add_location(request):
    return add_item(request, Location, 'location/add_location.html', 'location', ['name'])     

def add_farmer(request):
    return add_item(request, Farmer, 'farmer/add_farmer.html', 'farmer', ['name']) 

def add_animal_type(request):
    return add_item(request, AnimalType, 'animal_type/add_animal_type.html', 'animal_types', ['name'])

def add_farm(request):
    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'size': request.POST.get('size'),
            'location_id': request.POST.get('location'),
        }
        return add_object(request, Farm, data, 'farm') 
    locations=Location.objects.all()
    return render(request, 'farm/add_farm.html', {'locations': locations})

def add_animal(request):
    if request.method == 'POST':
        data = {
            'gender': request.POST.get('gender'),
            'health_status': request.POST.get('health_status'),
            'animal_type_id': request.POST.get('animal_type'),
        }
        return add_object(request, Animal, data, 'animal') 
    resources=Resource.objects.all()
    animal_types=AnimalType.objects.all()
    return render(request, 'animal/add_animal.html', {'animal_types':animal_types , 'resources': resources})

def add_resource(request):
    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'quantity': request.POST.get('quantity'),
            'expiration_date': request.POST.get('expiration_date'),
        }
        return add_object(request, Resource, data, 'resources')
    farms = Farm.objects.all()
    return render(request, 'resource/add_resource.html', {'farms': farms})

#edit functions
def edit_object_attributes(obj, data):
    for field, value in data.items():
        setattr(obj, field, value)
    obj.save()

def edit_farm(request, farm_id):
    farm = get_object_or_404(Farm, pk=farm_id)
    locations = Location.objects.all()
    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'location': Location.objects.get(pk=request.POST.get('location')),
            'size': request.POST.get('size'),
        }
        edit_object_attributes(farm, data)
        return redirect('farm')
    return render(request, 'farm/edit_farm.html', {'farm': farm, 'locations': locations})

def edit_farmer(request, farmer_id):
    farmer = get_object_or_404(Farmer, pk=farmer_id)
    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
        }
        edit_object_attributes(farmer, data)
        return redirect('farmer')
    return render(request, 'farmer/edit_farmer.html', {'farmer': farmer})

def edit_animal(request, animal_id):
    animal = get_object_or_404(Animal, pk=animal_id)
    animal_types = AnimalType.objects.all()
    resources = Resource.objects.all()
    if request.method == 'POST':
        data = {
            'gender': request.POST.get('gender'),
            'health_status': request.POST.get('health_status'),
            'animal_type': AnimalType.objects.get(id=request.POST.get('animal_type')),
        }
        animal.resources.clear()
        for resource_id in request.POST.getlist('resources'):
            animal.resources.add(Resource.objects.get(id=resource_id))
        edit_object_attributes(animal, data)
        return redirect('animal')
    return render(request, 'animal/edit_animal.html', {'animal': animal, 'animal_types': animal_types, 'resources': resources})

def edit_animal_type(request, animal_type_id):
    animal_type = get_object_or_404(AnimalType, pk=animal_type_id)
    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
        }
        edit_object_attributes(animal_type, data)
        return redirect('animal_types')
    return render(request, 'animal_type/edit_animal_type.html', {'animal_type': animal_type})

def edit_resource(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)
    farms = Farm.objects.all()
    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'quantity': request.POST.get('quantity'),
            'expiration_date': request.POST.get('expiration_date'),
        }
        edit_object_attributes(resource, data)
        farm_id = request.POST.get('farm')
        if farm_id:
            farm = get_object_or_404(Farm, pk=farm_id)
            resource.farm_resource.set([farm])
        return redirect('resources')
    return render(request, 'resource/edit_resource.html', {'resource': resource, 'farms': farms})

#delete functions
def delete_object(request, model, object_id, redirect_name, template_name):
    obj = get_object_or_404(model, pk=object_id)
    if request.method == 'POST':
        obj.delete()
        return redirect(redirect_name)
    return render(request, template_name, {model.__name__.lower(): obj})

def delete_farm(request, farm_id):
    return delete_object(request, Farm, farm_id, 'farm', 'farm/delete_farm.html')

def delete_farmer(request, farmer_id): 
    return delete_object(request, Farmer, farmer_id, 'farmer', 'farmer/delete_farmer.html')

def delete_animal(request, animal_id):
    return delete_object(request, Animal, animal_id, 'animal', 'animal/delete_animal.html')

def delete_animal_type(request, animal_type_id):
    return delete_object(request, AnimalType, animal_type_id, 'animal_types', 'animal_type/delete_animal_type.html')

def delete_resource(request, resource_id):
    return delete_object(request, Resource, resource_id, 'resources', 'resource/delete_resource.html')

def delete_location(request, location_id):
    return delete_object(request, Location, location_id, 'location', 'location/delete_location.html')