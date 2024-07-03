# JIRA Utility for Publishing Sprint Report(Python 2/n)
#### a. It should show How many EPIC , How many User Story and How many Sub-tasks are getting worked in the current Sprint

#### b. It should show User wise details How many EPIC , How many User Story and How many Sub-tasks are getting worked in the current Sprint [User,Count of Epic,Count of User Story,Count of Sub-tasks]

#### c. It should show User wise details How many User Story getting worked and their status counts in the current Sprint [User,Count of Open, Count of In Progress,Count of Resolved,Count of Closed]

#### d. It should show User wise details How many Sub-tasks getting worked and their status counts in the current Sprint [User,Count of Open, Count of In Progress,Count of Resolved,Count of Closed]

#### e. Show detailed table for each type with these columns [key,type,summary,assignee,created,duedate,status,last_comment] where key will have hyperlink with 'link' column value, separate table for each user

#### f. Show detailed table for each assign type with these columns [key,type,summary,assignee,created,duedate,status,last_comment] where key will have hyperlink with 'link' column value,separate table for each type


## For Development

```
git clone https://github.com/naren4b/my_jira.git
cd
 my_jira
 podman build --target dev Dockerfile_dev -t mypython
podman run -it -v ${PWD}:/work mypython sh # Powershell
podman run -it -v 'PWD':/work mypython sh #gitbash

/work # python --version
#pip install virtualenv
#python  -m venv env

source env/bin/activate
pip install pandas ,JIRA

cd jira

pip freeze > requirements.txt
pip install -r requirements.txt
```

# To Build the image

```
podman build . -t my_jira
```

# To RUN
1. Download the json with following command
```
podman run -v ${PWD}:/out --rm -d -e USERID=naren4b -e PASSWORD=password -e URI=jira.atlassian.com --name=my-jira my_jira
podman rm my-jira -f
```
#

# TODO
Python programme packaging
