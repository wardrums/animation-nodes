import bpy
from bpy.types import Node
from mn_node_base import AnimationNode
from mn_execution import nodePropertyChanged
from mn_utils import *
from mn_selection_utils import *

class mn_PropertyIn(bpy.types.PropertyGroup):
	property = bpy.props.StringProperty(name = "property", default = "", update = nodePropertyChanged)

class mn_PropertyInputNode(Node, AnimationNode):
	bl_idname = "mn_PropertyInputNode"
	bl_label = "Property Input"
	
	objectName = bpy.props.StringProperty(update = nodePropertyChanged)
	objects = bpy.props.CollectionProperty(type = mn_PropertyIn)
	showEditOptions = bpy.props.BoolProperty(default = True)
	
	def init(self, context):
		self.outputs.new("mn_ObjectListSocket", "Objects")
		
	def draw_buttons(self, context, layout):
		layout.prop(self, "showEditOptions", text = "Show Options")
		layout.separator()
        
		col = layout.column()
		row = col.row(align = True)
		row.prop_search(self, "objectName",  context.scene, "objects", icon="NONE", text = "")         
		selector = row.operator("mn.assign_active_object_to_node", text = "", icon = "EYEDROPPER")
		selector.nodeTreeName = self.id_data.name
		selector.nodeName = self.name
		selector.target = "objectName"
		col.separator()
         
		if self.showEditOptions:
			index = 0
			col = layout.column(align = True)
			for item in self.property:
				row = col.row(align = True)
			
				row.prop_search(item, "property",  context.scene, "objects", icon="NONE", text = "")  
				remove = row.operator("mn.remove_property_from_list_node", text = "", icon = "X")
				remove.nodeTreeName = self.id_data.name
				remove.nodeName = self.name
				remove.index = index
				index += 1
				
			add = layout.operator("mn.new_property_to_list_node", text = "New Item", icon = "PLUS")
			add.nodeTreeName = self.id_data.name
			add.nodeName = self.name
			
			add = layout.operator("mn.assign_active_object_to_node", text = "From Selection", icon = "PLUS")
			add.nodeTreeName = self.id_data.name
			add.nodeName = self.name
			
			layout.separator()
				
	def execute(self, input):
		output = {}
		output["Objects"] = self.getCurrentList()
		return output
		
	def getCurrentList(self):
		objectList = []
		for item in self.objects:
			objectList.append(bpy.data.objects.get(item.object))
		return objectList
		
	def addItemToList(self):
		item = self.objects.add()
		
	def removeItemFromList(self, index):
		self.objects.remove(index)
		
	def setObject(self, object, index):
		self.objects[index].object = object.name
		
	def newItemsFromList(self, names):
		for name in names:
			item = self.objects.add()
			item.object = name
	
	
