#
# parsing maven pom.xml
# artifactId, groupId and version
#
def vulcheck():
    import urllib.request, urllib.error, json, os
    from xml.etree import ElementTree

    isvul = False
    POM_FILE="pom.xml"  # replace your path
    namespaces = {'xmlns' : 'http://maven.apache.org/POM/4.0.0'}
    
    
    ElementTree.register_namespace('', "http://maven.apache.org/POM/4.0.0")
    tree = ElementTree.parse(POM_FILE)
    root = tree.getroot()
    
    deps = root.findall(".//xmlns:dependency", namespaces=namespaces)
    
    for d in deps:
        if d.find("xmlns:artifactId", namespaces=namespaces).text == 'jackson-dataformat-xml':
            artifactId = d.find("xmlns:artifactId", namespaces=namespaces)
            groupId    = d.find("xmlns:groupId", namespaces=namespaces)
            version    = d.find("xmlns:version", namespaces=namespaces)
            line       = groupId.text + ':' + artifactId.text + ':' + version.text
            #os.system("echo " + line + ">> listdeps.txt")
            url = "http://140.238.80.241/artifacts/" + artifactId.text + "-" + version.text + ".html"
            try:
                jsonurl = urllib.request.urlopen(url)
            except urllib.error.HTTPError as e:
                print('HTTPError: {}'.format(e.code))
            except urllib.error.URLError as e:
                print('URLError: {}'.format(e.reason))
            else:
                text = json.loads(jsonurl.read())
                #print(text["fixedVersion"].split(':')[1])
                version.text = text["fixedVersion"].split(':')[1]
                isvul = True
    #os.system("rm -f pomtest.xml")
    #tree.write("pomtest.xml")  
    exit(isvul)


