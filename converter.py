import rdflib
from rdflib import Graph, Namespace
import json
import os

def convert_xml_to_jsonld(input_data, output_file=None):
    """
    Convert XML to JSON-LD using rdflib
    
    Args:
        input_data: Either a filename (string) or XML content
        output_file: Optional filename to save the result
        
    Returns:
        JSON-LD as a Python dictionary
    """
    g = Graph()
    
    # Load and parse XML data
    if isinstance(input_data, str):
        if os.path.isfile(input_data):
            # Input is a file path
            try:
                g.parse(input_data, format="xml")
                print(f"Successfully parsed XML file with {len(g)} triples")
            except Exception as e:
                print(f"Error parsing XML file: {e}")
                return None
        elif '<rdf:RDF' in input_data or '<?xml' in input_data:
            # Input is XML content string
            try:
                g.parse(data=input_data, format="xml")
                print(f"Successfully parsed XML content with {len(g)} triples")
            except Exception as e:
                print(f"Error parsing XML content: {e}")
                return None
        else:
            print(f"Input doesn't appear to be a valid file path or XML content")
            return None
    
    # Define context with common namespaces
    context = {
        "cim": "http://iec.ch/TC57/CIM/CIM100#",
        "md": "http://iec.ch/TC57/61970-552/ModelDescription/1#",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "xsd": "http://www.w3.org/2001/XMLSchema#"
    }
    
    # Bind namespaces to the graph
    for prefix, uri in context.items():
        g.bind(prefix, Namespace(uri))
    
    # Serialize to JSON-LD
    try:
        jsonld_data = g.serialize(format="json-ld", context=context, indent=2)
        result = json.loads(jsonld_data)
        
        # Save to file if requested
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"JSON-LD data written to {output_file}")
        
        return result
    except Exception as e:
        print(f"Error serializing to JSON-LD: {e}")
        return None