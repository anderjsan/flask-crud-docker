import subprocess as sp

cmt = False
release = 0
feature = 0
fix = 0

# capture the ongoing commit message
last_commit = sp.run(["git", "log", "-1", "--pretty=%B"], capture_output=True, text=True).stdout.strip()
print(last_commit)
# check if the commit message contains the tag
if "[RELEASE]" in last_commit:
    release = 1
    cmt = True
elif "[FEATURE]" in last_commit:
    feature = 1
    cmt = True
elif "[FIX]" in last_commit:
    fix = 1
    cmt = True
elif "[INIT]" in last_commit:
    fix = 1
    cmt = True
else:
    cmt = False
    

#read the version file
with open(".version", "r") as f:
    current_version = f.readline().strip()
    print(current_version)

#increments the version according to the tag
current_version_parts = current_version.split(".")
current_version_parts[0] = str(int(current_version_parts[0]) + release)
current_version_parts[1] = str(int(current_version_parts[1]) + feature)
current_version_parts[2] = str(int(current_version_parts[2]) + fix)

#updates the version file
with open(".version", "w") as f:
    f.write(".".join(current_version_parts))
