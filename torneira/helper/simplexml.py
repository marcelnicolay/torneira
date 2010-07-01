from xml.dom.minidom import getDOMImplementation


def element_from_dict(document, elName, data):

	node = document.createElement(elName)
	
	for k, v in data.iteritems():
		
		if isinstance(v, dict):
			elem = element_from_dict(document, k, v)
		elif isinstance(v, list):
			elem = document.createElement(k)
			for item in v:
				elem.appendChild(element_from_dict(document, k[0:len(k)-1], item))
		elif isinstance(v, str):
			elem = document.createTextNode(v)
		node.appendChild(elem)
		
	return node

def dumps(data):
	
	rootName, rootValue = data.items()[0]
	implementation = getDOMImplementation()
	document = implementation.createDocument(None, rootName, None)
	
	rootNode = document.documentElement
	
	rootNode.appendChild(element_from_dict(document, rootName,  rootValue))
				
	return document.toxml()
