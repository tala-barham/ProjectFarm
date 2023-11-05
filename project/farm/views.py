from django.shortcuts import get_object_or_404, render,redirect
from.models import Farm,Farmer,Animal,AnimalType,Resource,Location
from .forms import LocationForm, FarmForm, FarmerForm, ResourceForm, AnimalTypeForm, AnimalForm

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

##edit,and function
def add_edit_item(request, model, form_class, template_name, redirect_name, instance_id=None):
    instance = None
    if instance_id:
        instance = model.objects.get(id=instance_id)
    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(redirect_name)
    else:
        form = form_class(instance=instance)
    return render(request, template_name, {'form': form, 'instance': instance})

#add functions
def add_location(request):
    return add_edit_item(request, Location, LocationForm, 'location/location_form.html', 'location')

def add_farmer(request):
    return add_edit_item(request, Farmer ,FarmerForm, 'farmer/farmer_form.html', 'farmer') 

def add_animal_type(request):
    return add_edit_item(request, AnimalType , AnimalTypeForm, 'animal_type/animal_type_form.html', 'animal_types')

def add_farm(request):
    return add_edit_item(request, Farm ,FarmForm, 'farm/farm_form.html', 'farm')

def add_animal(request):
    return add_edit_item(request, Animal, AnimalForm, 'animal/animal_form.html', 'animal')

def add_resource(request):
    return add_edit_item(request, Resource ,ResourceForm, 'resource/resource_form.html', 'resources')

#edit functions
def edit_location(request, location_id):
    return add_edit_item(request, Location, LocationForm, 'location/location_form.html', 'location', location_id)

def edit_farm(request, farm_id):
    return add_edit_item(request, Farm, FarmForm, 'farm/farm_form.html', 'farm', farm_id)

def edit_farmer(request, farmer_id):
    return add_edit_item(request, Farmer, FarmerForm, 'farmer/farmer_form.html', 'farmer', farmer_id )

def edit_animal(request, animal_id):
    return add_edit_item(request, Animal, AnimalForm, 'animal/animal_form.html', 'animal', animal_id)

def edit_animal_type(request, animal_type_id):
    return add_edit_item(request, AnimalType, AnimalTypeForm, 'animal_type/animal_type_form.html', 'animal_types', animal_type_id)

def edit_resource(request, resource_id):
    return add_edit_item(request, Resource, ResourceForm, 'resource/resource_form.html', 'resources', resource_id)

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