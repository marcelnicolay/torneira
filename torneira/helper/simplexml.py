# -*- coding: utf-8 -*-

# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.opensource.org/licenses/osl-3.0.php

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from xml.dom.minidom import getDOMImplementation, parseString

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

def dict_from_element(element, dic):
    
    if element.hasChildNodes():
        for node in element.childNodes:
            if node.nodeType == node.TEXT_NODE:
                dic[element.nodeName] = node.nodeValue
            else:
                if node.hasChildNodes and len(node.childNodes) == 1 and node.childNodes[0].nodeType == node.TEXT_NODE:
                    dic[node.nodeName] = node.childNodes[0].nodeValue
                else:
                    dic[node.nodeName] = dict_from_element(node, {})
        
    return dic

def dumps(data):
    rootName, rootValue = data.items()[0]
    implementation = getDOMImplementation()
    document = implementation.createDocument(None, rootName, None)

    rootNode = document.documentElement

    element_from_dict(document, rootNode,  rootValue)

    return document.toxml()

def loads(data):
    
    document = parseString(data)
    rootNode = document.documentElement
    
    dictionary = {}
    dictionary[rootNode.nodeName] = dict_from_element(rootNode, {})
    
    return dictionary
