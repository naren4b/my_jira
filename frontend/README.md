cp <out>/<name>.json data.json
podman build . -t my_jira_report
podman run --rm -d --network host --name=my-jira-report my_jira_report
podman rm my-jira-report -f