import bpy

enableSelectionSorting = True

sortedSelectionNames = []

def getSortedSelectedObjectNames():
	return sortedSelectionNames

def updateSelectionSorting():
	global sortedSelectionNames
	
	selectedNames = getSelectedObjectNames()
	
	if enableSelectionSorting:
		newSortedSelection = []
		for name in sortedSelectionNames:
			if name in selectedNames:
				newSortedSelection.append(name)
		for name in selectedNames:
			if name not in newSortedSelection:
				newSortedSelection.append(name)
		sortedSelectionNames = newSortedSelection
	else:
		sortedSelectionNames = selectedNames		
	
def getSelectedObjectNames():
	selectedNames = []
	for object in bpy.context.selected_objects:
		selectedNames.append(object.name)
	return selectedNames