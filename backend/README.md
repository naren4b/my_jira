# Consuming JIRA api with Python and NodeJS Podman Reports

# For Development

```
cd
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

podman run -v ${PWD}:/out --rm -d -e USERID=naren4b -e PASSWORD=password -e URI=jira.atlassian.com --name=my-jira my_jira
podman rm my-jira -f

#

#TODO
Python programme packaging
