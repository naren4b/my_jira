import pandas as pd
import json
from datetime import datetime, timedelta
import os, sys

# report_id = sys.argv[1]


# Load and flatten JSON data
def load_and_flatten_json(file_path):
    with open(file_path, "r") as file:
        json_data = json.load(file)

    # Flatten the nested lists
    flattened_data = [item for sublist in json_data for item in sublist]
    return flattened_data


# Report generation functions
def report_issue_counts(data):
    issue_counts = data["type"].value_counts().reset_index()
    issue_counts.columns = ["Type", "Count"]
    return issue_counts


def report_user_issue_counts(data):
    user_issue_counts = (
        data.groupby(["assignee", "type"]).size().unstack(fill_value=0).reset_index()
    )
    return user_issue_counts


def report_user_story_status_counts(data):
    user_story_status_counts = (
        data[data["type"] == "User Story"]
        .groupby(["assignee", "status"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    return user_story_status_counts


def report_sub_task_status_counts(data):
    sub_task_status_counts = (
        data[data["type"] == "Sub-task"]
        .groupby(["assignee", "status"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    return sub_task_status_counts


def report_latest_updates(data):
    latest_updates = data[
        [
            "key",
            "type",
            "summary",
            "assignee",
            "created",
            "duedate",
            "status",
            "last_comment",
            "link",
        ]
    ]
    return latest_updates


# Main function
def generate_report(report_id):
    output_dir = "out/" + report_id
    os.makedirs(output_dir, exist_ok=True)
    json_file_path = os.path.join(output_dir, f"data_{report_id}.json")
    data_list = load_and_flatten_json(json_file_path)
    data = pd.DataFrame(data_list)

    # Generate and save reports
    report_a = report_issue_counts(data)
    report_a.to_csv(
        os.path.join(output_dir, f"report_a_issue_counts_{report_id}.csv"), index=False
    )

    report_b = report_user_issue_counts(data)
    report_b.to_csv(
        os.path.join(output_dir, f"report_b_user_issue_counts_{report_id}.csv"),
        index=False,
    )

    report_c = report_user_story_status_counts(data)
    report_c.to_csv(
        os.path.join(output_dir, f"report_c_user_story_status_counts_{report_id}.csv"),
        index=False,
    )

    report_d = report_sub_task_status_counts(data)
    report_d.to_csv(
        os.path.join(output_dir, f"report_d_sub_task_status_counts_{report_id}.csv"),
        index=False,
    )

    report_e = report_latest_updates(data)
    report_e.to_csv(
        os.path.join(output_dir, f"report_e_latest_updates_{report_id}.csv"),
        index=False,
    )

    print("Reports have been saved to the specified directory.")


# generate_report(report_id)
