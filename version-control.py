import subprocess as sp
import json
class CommitUpdater:
    def __init__(self) -> None:
        self.commit_keywords = {
            "[RELEASE]": 0,
            "[FEATURE]": 1,
            "[INIT]": 1, # Assuming [INIT] should increment the FIX term
            "[FIX]": 2

        }
        self.version_terms = [0,0,0]
        self.last_tag = [0,0,1]
        self.new_tag = [0,0,1]
        self.keyword = ""
        self.commit_message = ""
        
    def get_curr_version(self):
        # get the last version
        with open(".version", "r") as f:
            # check if the file is empty
            if not f.read(1):
                last_version = "0.0.0"
            else:
                last_version = f.readline().strip()
        
        last_version_parts = last_version.split(".")
        self.last_tag = last_version_parts
        return last_version_parts

        
    def set_version_terms(self):
        # capture the last commit.
        self.commit_message = sp.run(["git", "log", "-1", "--pretty=%B"], capture_output=True, text=True, encoding='utf-8').stdout.strip()
        
        # get the commit type
        for keyword, index in self.commit_keywords.items():
            if keyword in self.commit_message:
                self.version_terms[index] += 1
                self.keyword = keyword
                break

    def set_new_version(self, tag):
        # aplicar o calculo da nova versão:
        # Increment version
        new_tag = tag
        if x.version_terms[0] > 0:
            new_tag[0] = str(int(new_tag[0]) + x.version_terms[0])
            new_tag[1] = '0'
            new_tag[2] = '0'
        elif x.version_terms[1] > 0:
            new_tag[1] = str(int(new_tag[1]) + x.version_terms[1])
            new_tag[2] = '0'
        elif x.version_terms[2] > 0:
            new_tag[2] = str(int(new_tag[2]) + x.version_terms[2])

        new_version = ".".join(new_tag)
        with open(".version", "w") as f:
            f.write(new_version)
        self.new_tag = new_tag
        return new_version

    
    def log_verson(self, tag, keyword, message):
        commit_log = []
        # open version_log and feed an array of commits.
        with open(".version_log", "r") as json_file:
            # if file is empty, create an empty list.
            if json_file.read() == "":
                commit_logs = []
            else: 
                commit_logs = json.load(json_file)
        
        #prepare a new commit_log to enter into commit_log list.
        if keyword == "[FIX]":
            commit_log = {
                "tag": tag,
                "git_message": f"{message}"
            }
        else:
            commit_log = {
                "tag": tag,
                "git_message": f"{message}",
                "fixes": []
            }
        
        #if keyword means FIX, search for the FEATURE or release tag where this fix was belongs to. Add this commit_log into the commit_logs list under FIXES, respecting the parenthood
        if keyword in ("[FIX]"):
            for commit in reversed(commit_logs):
                # se os dois primeiros termos da tag são iguais, faça o append do commit_log.
                # Separando os dois primeiros termos das tags
                existing_tag_terms = commit["tag"].split(".")[:2]
                new_tag_terms = tag.split(".")[:2]

                # Verificando se os dois primeiros termos são iguais
                if existing_tag_terms == new_tag_terms:
                    commit["fixes"].append(commit_log)
                    break
        else:
            commit_logs.append(commit_log)
        
        #save commit_logs into version_log file
        with open(".version_log", "w") as json_file:
            json.dump(commit_logs, json_file)

        print(commit_logs)
                
                

        #if not, add a new commit_log to the commit_logs list, with FIXES as an empty inner list

    

x = CommitUpdater()
x.set_version_terms()
vers = x.get_curr_version()
tag = x.set_new_version(vers)
x.log_verson(tag,x.keyword,x.commit_message)
