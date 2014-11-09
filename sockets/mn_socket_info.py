import mn_node_base

listChains = [
	["mn_FloatSocket", "mn_FloatListSocket"],
	["mn_ObjectSocket", "mn_ObjectListSocket"],
	["mn_StringSocket", "mn_StringListSocket"],
	["mn_GenericSocket", "mn_GenericSocket"] ]
	
def getListSocketType(socketType):
	for listChain in listChains:
		if socketType in listChain:
			index = listChain.index(socketType)
			if index == len(listChain) - 1: return None
			return listChain[index + 1]
	return None
	
def hasListSocketType(socketType):
	return not getListSocketType(socketType) == None
	
def getSocketNameByDataType(dataType):
	subClasses = mn_node_base.mn_BaseSocket.__subclasses__()
	for subClass in subClasses:
		if getattr(subClass, "dataType") == dataType: return subClass.bl_idname
	return None