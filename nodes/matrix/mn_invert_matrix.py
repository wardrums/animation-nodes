import bpy
from bpy.types import Node
from mathutils import *
from mn_node_base import AnimationNode
from mn_execution import nodePropertyChanged, allowCompiling, forbidCompiling


class mn_InvertMatrix(Node, AnimationNode):
	bl_idname = "mn_InvertMatrix"
	bl_label = "Invert Matrix"
	
	def init(self, context):
		forbidCompiling()
		self.inputs.new("mn_MatrixSocket", "Matrix")
		self.outputs.new("mn_MatrixSocket", "Inverted Matrix")
		allowCompiling()
		
	def draw_buttons(self, context, layout):
		layout.separator()
		
	def getInputSocketNames(self):
		return {"Matrix" : "matrix"}
	def getOutputSocketNames(self):
		return {"Inverted Matrix" : "matrix"}

	def useInLineExecution(self):
		return True
	def getInLineExecutionString(self, outputUse):
		return "$matrix$ = %matrix%.inverted(mathutils.Matrix.Identity(4))"
		
	def getModuleList(self):
		return ["mathutils"]