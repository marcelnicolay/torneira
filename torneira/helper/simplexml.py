from xml.dom.minidom import getDOMImplementation


def element_from_dict(document, elRoot, data):

	for k, v in data.iteritems():
		
		elem = document.createElement(k)
		
		if isinstance(v, dict):
			element_from_dict(document, elem, v)
		elif isinstance(v, list):
			elem = document.createElement(k)
			for item in v:
				elItem = document.createElement(k[0:len(k)-1])
				element_from_dict(document, elItem, item)
				elem.appendChild(elItem)
		elif isinstance(v, str):
			elem.appendChild(document.createCDATASection(v))
		else:
			elem.appendChild(document.createTextNode(str(v)))
						
		elRoot.appendChild(elem)
		
def dumps(data):
	
	rootName, rootValue = data.items()[0]
	implementation = getDOMImplementation()
	document = implementation.createDocument(None, rootName, None)
	
	rootNode = document.documentElement
	
	element_from_dict(document, rootNode,  rootValue)
				
	return document.toxml()
