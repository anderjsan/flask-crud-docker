import subprocess as sp

cmt = False
commit_keywords = {
    "[RELEASE]": 0,
    "[FEATURE]": 1,
    "[FIX]": 2,
    "[INIT]": 2  # Supondo que [INIT] deve incrementar o termo de correção
}

version_terms = [0, 0, 0]

# capture the ongoing commit message
last_commit = sp.run(["git", "log", "-1", "--pretty=%B"], capture_output=True, text=True).stdout.strip()
print(last_commit)
# check if the commit message contains the tag
cmt = False
for keyword, index in commit_keywords.items():
    if keyword in last_commit:
        version_terms[index] += 1
        cmt = True
        break
    

#read the version file
with open(".version", "r") as f:
    current_version = f.readline().strip()
    print(current_version)

#increments the version according to the tag
current_version_parts = current_version.split(".")
current_version_parts[0] = str(int(current_version_parts[0]) + version_terms[0])
current_version_parts[1] = str(int(current_version_parts[1]) + version_terms[1])
current_version_parts[2] = str(int(current_version_parts[2]) + version_terms[2])

#updates the version file
with open(".version", "w") as f:
    f.write(".".join(current_version_parts))
