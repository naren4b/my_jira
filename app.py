import sys
import os
from datetime import datetime
import json
from jira import JIRA

import pandas as pd

import argparse
import report

user = os.environ["USERID"]  # sys.argv[1]
password = os.environ["PASSWORD"]  # sys.argv[2]
uri = os.environ["URI"]  ## sys.argv[3]
merged_data = []


# user = sys.argv[1]
# password = sys.argv[2]
# uri = sys.argv[3]
server = "https://" + uri
report_id = datetime.now().strftime("%Y%m%d-%H%M%S")

print("server :" + server)

options = {"server": server}
output_dir = "out/" + report_id
os.makedirs(output_dir, exist_ok=True)
jira = JIRA(options, basic_auth=(user, password))


def merge_json_files():
    data_json = os.path.join(output_dir, f"data_{report_id}.json")
    data_csv = os.path.join(output_dir, f"data_{report_id}.csv")
    with open(data_json, "w") as file:
        json.dump(merged_data, file, indent=4)
    print(f"Report Generated {data_json}")
    to_csv(data_json, data_csv)


def to_csv(filename_json, filename_csv):
    df = pd.read_json(filename_json)
    df.to_csv(filename_csv, index=False)
    print(f"CSV report has been created at {filename_csv}")


def get_issue_Link(key):
    return server + f"/browse/" + key


def trim_string(string, length=50):
    """Trim the string to the specified length and append '...' if it exceeds that length."""
    if len(string) > length:
        return string[: length - 3] + "..."
    return string


def save_issues_to_file(type, issues, filename_json, filename_csv):
    with open(filename_json, "w") as file:
        json.dump(issues, file, indent=4)
    print(f"Issues saved to {filename_json}")
    to_csv(filename_json, filename_csv)


def get_formatted_date(adate):
    return datetime.strptime(adate, "%Y-%m-%dT%H:%M:%S.%f%z") if adate else "NA"


def fetch_jira_issues(type, jql_query):
    issues = jira.search_issues(jql_str=jql_query, maxResults=1000)
    print(f"No of ", type, " Issues:", len(issues))
    issues_data = []
    for issue in issues:
        # print(server + "/rest/api/2/issue/" + issue.key)
        last_comment = (
            issue.fields.comment.comments[-1].body
            if issue.fields.comment.comments
            else "No comments"
        )
        duedate = issue.fields.duedate
        if duedate:
            duedate = datetime.strptime(duedate, "%Y-%m-%d").strftime("%d-%m-%Y")
        else:
            duedate = "No due date"
        created = datetime.strptime(
            issue.fields.created, "%Y-%m-%dT%H:%M:%S.%f%z"
        ).strftime("%d-%m-%Y")
        issues_data.append(
            {
                "key": issue.key,
                "type": issue.fields.issuetype.name,
                "summary": trim_string(issue.fields.summary),
                "assignee": (
                    issue.fields.assignee.displayName
                    if issue.fields.assignee
                    else "Unassigned"
                ),
                "created": created,
                "duedate": duedate,
                "status": issue.fields.status.name,
                "last_comment": trim_string(last_comment),
                "link": get_issue_Link(issue.key),
                #                "parent": issue.fields.parent,
            }
        )
    return issues_data


def main():
    report_types = {
        "epic": "assignee = currentUser() and type = Epic AND Sprint in openSprints()",
        "us": "assignee = currentUser() and type = 'User Story' AND Sprint in openSprints()",
        "st": "assignee = currentUser() and type = 'Sub-task' AND Sprint in openSprints()",
    }

    for type, jql_query in report_types.items():
        print("Report: " + report_id)
        filename_json = os.path.join(output_dir, f"{type}_issues_{report_id}.json")
        filename_csv = os.path.join(output_dir, f"{type}_issues_{report_id}.csv")
        data = fetch_jira_issues(type, jql_query)
        merged_data.append(data)
        save_issues_to_file(type, data, filename_json, filename_csv)
    merge_json_files()
    report.generate_report(report_id)


if __name__ == "__main__":
    main()
