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
            url = "http://140.238.80.241/artifacts/" + artifactId.text + "-" + version.text + ".html"
            try:
                jsonurl = urllib.request.urlopen(url)
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    print("healty : "+artifactId.text+":"+version.text)
                else:
                    print('HTTPError: {}'.format(e.code))
            except urllib.error.URLError as e:
                print('URLError: {}'.format(e.reason))
            else:
                text = json.loads(jsonurl.read())
                version.text = text["fixedVersion"].split(':')[1]
                isvul = True
    os.system("rm -f pom.xml")
    tree.write("pom.xml")
    exit(isvul)

def patch():
    import os
    
    origbranch = os.popen('echo ${CI_COMMIT_REF_NAME}').read().strip()
    token = os.popen('echo ${CI_TOKEN}').read().strip()
    remoteurl = os.popen('echo ${REMOTE_URL}').read().strip()
    os.system("git remote set-url origin https://gitlab-ci-token:" + token + "@" + remoteurl)
    os.system("git checkout -b ${CI_COMMIT_REF_NAME}_remediation")
    os.system('git add pom.xml && git commit -m "vulnerabilities remediation suggestion for ${CI_COMMIT_REF_NAME}"')
    code, out, err = runcommand('git push origin ${CI_COMMIT_REF_NAME}_remediation -o merge_request.create -o merge_request.target=' + origbranch + ' -o merge_request.remove_source_branch -o merge_request.title="vulnerabilities remediation suggestion for ${CI_COMMIT_REF_NAME} " -o merge_request.description=".. we have to add the list of dependencies with r"')
    if code != 0:
        print(err)
        exit(True)
    else:
        print(out)
        exit(False)

def runcommand (cmd):
    import os, subprocess
    proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True,
                            universal_newlines=True)
    std_out, std_err = proc.communicate()
    return proc.returncode, std_out, std_err



