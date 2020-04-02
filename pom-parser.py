#
# parsing maven pom.xml
# artifactId, groupId and version
#
from xml.etree import ElementTree

POM_FILE="pom.xml"  # replace your path
namespaces = {'xmlns' : 'http://maven.apache.org/POM/4.0.0'}

tree = ElementTree.parse(POM_FILE)
root = tree.getroot()

deps = root.findall(".//xmlns:dependency", namespaces=namespaces)
for d in deps:
    artifactId = d.find("xmlns:artifactId", namespaces=namespaces)
    groupId    = d.find("xmlns:groupId", namespaces=namespaces)
    if d.find("xmlns:version", namespaces=namespaces) is not None:
        version = d.find("xmlns:version", namespaces=namespaces)
        print(groupId.text + ':' + artifactId.text + ':' + version.text)
    else:
        print(groupId.text + ':' + artifactId.text)