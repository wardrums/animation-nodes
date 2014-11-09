import bpy
from bpy.types import Node
from mathutils import *
from mn_node_base import AnimationNode
from mn_execution import nodePropertyChanged, allowCompiling, forbidCompiling


class mn_MatrixConvert(Node, AnimationNode):
	bl_idname = "mn_MatrixConvert"
	bl_label = "Convert Matrix"
	outputUseParameterName = "useOutput"
	
	def init(self, context):
		forbidCompiling()
		self.inputs.new("mn_MatrixSocket", "Matrix")
		self.outputs.new("mn_VectorSocket", "Translation")
		self.outputs.new("mn_VectorSocket", "Rotation")
		self.outputs.new("mn_VectorSocket", "Scale")
		allowCompiling()
		
	def getInputSocketNames(self):
		return {"Matrix" : "matrix"}
	def getOutputSocketNames(self):
		return {"Translation" : "translation",
				"Rotation" : "rotation",
				"Scale" : "scale"}

	def useInLineExecution(self):
		return True
	def getInLineExecutionString(self, outputUse):
		codeLines = []
		if outputUse["Translation"]: codeLines.append("$translation$ = %matrix%.to_translation()")
		if outputUse["Rotation"]: codeLines.append("$rotation$ = %matrix%.to_euler()")
		if outputUse["Scale"]: codeLines.append("$scale$ = %matrix%.to_scale()")
		return "\n".join(codeLines)