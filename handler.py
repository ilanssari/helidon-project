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
    os.system("rm -f pom.xml")
    tree.write("pom.xml")
    exit(isvul)

def patche():
    import os 
    
    origbranch = os.popen('echo ${CI_COMMIT_REF_NAME}').read()
    token = os.popen('echo ${CI_TOKEN}').read()
    remoteurl = os.popen('echo ${REMOTE_URL}').read()
    print(os.popen("echo 'https://gitlab-ci-token:" + token + "@" + remoteurl + "'").read())
    #os.system("git remote set-url origin https://gitlab-ci-token:" + token + "@" + remoteurl)
    #os.system("git checkout -b patch-${CI_COMMIT_REF_NAME}-${CI_COMMIT_SHA}")
    #os.system('git add pom.xml && git commit -m "patche vulnerabilities for ${CI_COMMIT_REF_NAME}"')
    #os.system('git push origin patch-${CI_COMMIT_REF_NAME}-${CI_COMMIT_SHA} -o merge_request.create -o merge_request.target=' + origbranch + ' -o merge_request.remove_source_branch -o merge_request.title="patche vulnerabilities" -o merge_request.description="patche vulnerabilities"')


