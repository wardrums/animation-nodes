import bpy
from mn_utils import *
from mn_cache import *
	
# names
		
def getPossibleObjectName(name = "object"):
	randomString = getRandomString(3)
	counter = 1
	while bpy.data.objects.get(name + randomString + str(counter)) is not None:
		counter += 1
	return name + randomString + str(counter)