#PyGithub
#http://pygithub.readthedocs.io/en/latest/index.html

from github import Github
import os
import argparse
from datetime import datetime, timedelta

parser = argparse.ArgumentParser(description='Generate github repo and upload Dockerfile/CWL')
parser.add_argument('--token', dest='token', help='your github token')
parser.add_argument('--org', dest='org', help='the github organization to make repositories in')
parser.add_argument('--tool', dest='tool', help='the tool being registered')
parser.add_argument('--tag', action='append', dest='tag', help='the tags to apply to the repo')

args = parser.parse_args()

#g = Github("github handle", "password") #OR
g = Github(args.token)

user = g.get_user()
organization = g.get_organization(args.org)

# create repo
try:
    print ("Creating repo: "+args.tool+" in org: "+args.org)
    repo = organization.create_repo(name=args.tool, description="Pfda2Dockstore Github repo for tool "+args.tool,
                            homepage="https://github.com", private=False,
                            has_issues=False, has_wiki=False, has_downloads=False )
    # loop over each tag
    # NOTE: you probably have different files for each tag!
    for tag in args.tag:
        # create files in repo
        file_list = ['./Dockstore.cwl','./Dockerfile']
        for entry in file_list:
            with open(entry, 'rb') as input_file:
                data = input_file.read()
                file_path = '/'+ os.path.basename(input_file.name)
                print (" + creating file:" + file_path)
                repo.create_file(file_path, "initial commit", str(data))
        since = datetime.now() - timedelta(days=1)
        commits = repo.get_commits(since=since)
        last = commits[0]
        print (last)
        repo.create_git_tag(tag, 'the tag message', last, 'commit')

except:
    print("errors creating repo, check to ensure this is not a duplicate")
