import bpy, time
from bpy.app.handlers import persistent
from mn_utils import *
from mn_cache import clearExecutionCache
from mn_network_code_generator import getAllNetworkCodeStrings

ALLOW_COMPILING = True

compiledCodeObjects = []
codeStrings = []

def updateAnimationTrees(treeChanged = True):
	if ALLOW_COMPILING:
		forbidCompiling()
		start = time.clock()
		if treeChanged:
			rebuildNodeNetworks()
		for i, codeObject in enumerate(compiledCodeObjects):
			if bpy.context.scene.showFullError: 
				exec(codeObject, {})
			else:
				try: exec(codeObject, {})
				except BaseException as e:
					rebuildNodeNetworks()
					try: exec(codeObject, {})
					except BaseException as e: print(e)
		clearExecutionCache()
		if bpy.context.scene.printUpdateTime:
			timeSpan = time.clock() - start
			print("Exec. " + str(round(timeSpan, 7)) + " s  -  " + str(round(1/timeSpan, 5)) + " fps")
		allowCompiling()
			
def allowCompiling():
	global ALLOW_COMPILING
	ALLOW_COMPILING = True
def forbidCompiling():
	global ALLOW_COMPILING
	ALLOW_COMPILING = False
			
			
# compile code objects
################################

def rebuildNodeNetworks():
	global compiledCodeObjects, codeStrings
	del compiledCodeObjects[:]
	del codeStrings[:]
	try:
		codeStrings = getAllNetworkCodeStrings()
		for code in codeStrings:
			compiledCodeObjects.append(compile(code, "<string>", "exec"))
	except:
		pass
				
		
# Force Cache Rebuilding Panel
##############################
		
class AnimationNodesPanel(bpy.types.Panel):
	bl_idname = "mn.settings_panel"
	bl_label = "Animation Nodes"
	bl_space_type = "NODE_EDITOR"
	bl_region_type = "UI"
	
	def draw(self, context):
		layout = self.layout
		layout.operator("mn.force_full_update")
		layout.operator("mn.print_node_tree_execution_string")
		scene = context.scene
		layout.label("Update when:")
		layout.prop(scene, "updateAnimationTreeOnFrameChange", text = "Frames Changes")
		layout.prop(scene, "updateAnimationTreeOnSceneUpdate", text = "Scene Updates")
		layout.prop(scene, "updateAnimationTreeOnPropertyChange", text = "Property Changes")
		layout.prop(scene, "printUpdateTime", text = "Print Update Time")
		layout.prop(scene, "showFullError", text = "Show Full Error")
		layout.prop(scene, "nodeExecutionProfiling", text = "Node Execution Profiling")
		
		layout.separator()
		node = bpy.context.active_node
		if node is not None:
			layout.label("Name: " + node.name)
			addToUi = layout.operator("mn.set_node_input_in_ui")
			addToUi.nodeTreeName = node.id_data.name
			addToUi.nodeName = node.name
			addToUi.socketIdentifier = node.inputs[0].identifier
			
class AnimationNodesSettingsPanel(bpy.types.Panel):
	bl_idname = "mn.property_panel"
	bl_label = "Node Settings"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "Animation"
	bl_context = "objectmode"
	
	def draw(self, context):
		layout = self.layout
		for item in bpy.context.scene.nodeInputsInUi:
			nodeTree = bpy.data.node_groups.get(item.nodeTreeName)
			if nodeTree is None: continue
			node = nodeTree.nodes.get(item.nodeName)
			if node is None: continue
			socket = getInputSocketByIdentifier(node, item.socketIdentifier)
			if socket is None: continue
			socket.draw(context, layout, node, "")
			
def getInputSocketByIdentifier(node, identifier):
	for socket in node.inputs:
		if socket.identifier == identifier: return socket
	return None
			
		
		
class ForceNodeTreeUpdate(bpy.types.Operator):
	bl_idname = "mn.force_full_update"
	bl_label = "Force Node Tree Update"

	def execute(self, context):
		updateAnimationTrees(treeChanged = True)
		return {'FINISHED'}
		
class PrintNodeTreeExecutionStrings(bpy.types.Operator):
	bl_idname = "mn.print_node_tree_execution_string"
	bl_label = "Print Node Tree Code"

	def execute(self, context):
		print()
		for codeString in codeStrings:
			print(codeString)
			print()
			print("-"*80)
			print()
		return {'FINISHED'}
		
class SetNodeInputInUi(bpy.types.Operator):
	bl_idname = "mn.set_node_input_in_ui"
	bl_label = "Set Node Input in UI"
	
	nodeTreeName = bpy.props.StringProperty()
	nodeName = bpy.props.StringProperty()
	socketIdentifier = bpy.props.StringProperty()

	def execute(self, context):
		item = bpy.context.scene.nodeInputsInUi.add()
		item.nodeTreeName = self.nodeTreeName
		item.nodeName = self.nodeName
		item.socketIdentifier = self.socketIdentifier
		return {'FINISHED'}
	
class NodeInputToUIPropertyGroup(bpy.types.PropertyGroup):
	nodeTreeName = bpy.props.StringProperty(name = "Node Tree Name")
	nodeName = bpy.props.StringProperty(name = "Highest Frequency")
	socketIdentifier = bpy.props.StringProperty(name = "Socket Identifier")
	
		
# handlers to start the update
##############################

bpy.types.Scene.updateAnimationTreeOnFrameChange = bpy.props.BoolProperty(default = True, name = "Update Animation Tree On Frame Change")
bpy.types.Scene.updateAnimationTreeOnSceneUpdate = bpy.props.BoolProperty(default = True, name = "Update Animation Tree On Scene Update")
bpy.types.Scene.updateAnimationTreeOnPropertyChange = bpy.props.BoolProperty(default = True, name = "Update Animation Tree On Property Change")

bpy.types.Scene.printUpdateTime = bpy.props.BoolProperty(default = False, name = "Print Update Time")
bpy.types.Scene.showFullError = bpy.props.BoolProperty(default = False, name = "Show Full Error")
bpy.types.Scene.nodeExecutionProfiling = bpy.props.BoolProperty(default = False, name = "Node Execution Profiling")
	
@persistent
def frameChangeHandler(scene):
	if scene.updateAnimationTreeOnFrameChange:
		updateAnimationTrees(False)
@persistent
def sceneUpdateHandler(scene):
	if scene.updateAnimationTreeOnSceneUpdate:
		updateAnimationTrees(False)
@persistent
def fileLoadHandler(scene):
	updateAnimationTrees(True)
def nodePropertyChanged(self, context):
	if context.scene.updateAnimationTreeOnPropertyChange:
		updateAnimationTrees(False)
def nodeTreeChanged():
	updateAnimationTrees(True)

	
bpy.app.handlers.frame_change_post.append(frameChangeHandler)
bpy.app.handlers.scene_update_post.append(sceneUpdateHandler)
bpy.app.handlers.load_post.append(fileLoadHandler)
		
		
# register
################################
		
def register():
	bpy.utils.register_module(__name__)
	bpy.types.Scene.nodeInputsInUi = bpy.props.CollectionProperty(type = NodeInputToUIPropertyGroup)

def unregister():
	bpy.utils.unregister_module(__name__)