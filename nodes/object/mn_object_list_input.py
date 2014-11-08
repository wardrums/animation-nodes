import bpy
from bpy.types import Node
from mn_node_base import AnimationNode
from mn_execution import nodePropertyChanged
from mn_utils import *
from mn_selection_utils import *

class mn_ObjectPropertyGroup(bpy.types.PropertyGroup):
	object = bpy.props.StringProperty(name = "Object", default = "", update = nodePropertyChanged)

class mn_ObjectListInputNode(Node, AnimationNode):
	bl_idname = "mn_ObjectListInputNode"
	bl_label = "Object List"
	
	objects = bpy.props.CollectionProperty(type = mn_ObjectPropertyGroup)
	showEditOptions = bpy.props.BoolProperty(default = True)
	
	def init(self, context):
		self.outputs.new("mn_ObjectListSocket", "Objects")
		
	def draw_buttons(self, context, layout):
		layout.prop(self, "showEditOptions", text = "Show Options")
		layout.separator()
		if self.showEditOptions:
			index = 0
			col = layout.column(align = True)
			for item in self.objects:
				row = col.row(align = True)
				select = row.operator("mn.assign_active_object_to_list_node", text = "", icon = "EYEDROPPER")
				select.nodeTreeName = self.id_data.name
				select.nodeName = self.name
				select.index = index
				row.prop_search(item, "object",  context.scene, "objects", icon="NONE", text = "")  
				remove = row.operator("mn.remove_property_from_out_list_node", text = "", icon = "X")
				remove.nodeTreeName = self.id_data.name
				remove.nodeName = self.name
				remove.index = index
				index += 1
				
			add = layout.operator("mn.new_property_to_out_list_node", text = "New Item", icon = "PLUS")
			add.nodeTreeName = self.id_data.name
			add.nodeName = self.name
			
			add = layout.operator("mn.selected_objects_to_object_list_node", text = "From Selection", icon = "PLUS")
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
	
	
class AssignActiveObjectToListNode(bpy.types.Operator):
	bl_idname = "mn.assign_active_object_to_list_node"
	bl_label = "Assign Active Object"
	
	nodeTreeName = bpy.props.StringProperty()
	nodeName = bpy.props.StringProperty()
	index = bpy.props.IntProperty()
	
	@classmethod
	def poll(cls, context):
		return getActive() is not None
		
	def execute(self, context):
		obj = getActive()
		node = getNode(self.nodeTreeName, self.nodeName)
		node.setObject(obj, self.index)
		return {'FINISHED'}	
		
class SelectedObjectsToObjectListNode(bpy.types.Operator):
	bl_idname = "mn.selected_objects_to_object_list_node"
	bl_label = "New Items From Selection"
	
	nodeTreeName = bpy.props.StringProperty()
	nodeName = bpy.props.StringProperty()
		
	def execute(self, context):
		node = getNode(self.nodeTreeName, self.nodeName)
		node.newItemsFromList(getSortedSelectedObjectNames())
		return {'FINISHED'}	
	
class mn_NewPropertyOutListNode(bpy.types.Operator):
	bl_idname = "mn.new_property_to_out_list_node"
	bl_label = "New String Property to String List Node"
	
	nodeTreeName = bpy.props.StringProperty()
	nodeName = bpy.props.StringProperty()
	
	def execute(self, context):
		node = getNode(self.nodeTreeName, self.nodeName)
		node.addItemToList()
		return {'FINISHED'}
		
class mn_RemovePropertyFromOutListNode(bpy.types.Operator):
	bl_idname = "mn.remove_property_from_out_list_node"
	bl_label = "Remove String Property from String List Node"
	
	nodeTreeName = bpy.props.StringProperty()
	nodeName = bpy.props.StringProperty()
	index = bpy.props.IntProperty()
	
	def execute(self, context):
		node = getNode(self.nodeTreeName, self.nodeName)
		node.removeItemFromList(self.index)
		return {'FINISHED'}
		
