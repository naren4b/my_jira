import pandas as pd
import glob
import json
import os, sys


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
    # Create a new column with hyperlink for the 'key'
    latest_updates["key"] = latest_updates.apply(
        lambda x: f'<a href="{x["link"]}" target="_blank">{x["key"]}</a>', axis=1
    )
    return latest_updates


# Function to save reports to CSV files and create HTML content
def save_reports_and_create_html(data, output_dir, template_file):
    # Generate reports
    report_a = report_issue_counts(data)
    report_b = report_user_issue_counts(data)
    report_c = report_user_story_status_counts(data)
    report_d = report_sub_task_status_counts(data)
    report_e = report_latest_updates(data)

    # Convert reports to HTML tables
    report_a_html = report_a.to_html(
        index=False, classes="table table-sortable", escape=False
    )
    report_b_html = report_b.to_html(
        index=False, classes="table table-sortable", escape=False
    )
    report_c_html = report_c.to_html(
        index=False, classes="table table-sortable", escape=False
    )
    report_d_html = report_d.to_html(
        index=False, classes="table table-sortable", escape=False
    )
    report_e_html = report_e.to_html(
        index=False, classes="table table-sortable", escape=False
    )

    # Load HTML template
    with open(template_file, "r") as file:
        html_template = file.read()

    # Insert report tables into the HTML template
    html_content = html_template.format(
        report_a=report_a_html,
        report_b=report_b_html,
        report_c=report_c_html,
        report_d=report_d_html,
        report_e=report_e_html,
    )

    # Save HTML content to file
    with open(f"{output_dir}/report.html", "w") as file:
        file.write(html_content)

    print("Reports have been saved to the specified directory and HTML file created.")


# Load and flatten JSON data
def load_and_flatten_json(file_path):
    with open(file_path, "r") as file:
        json_data = json.load(file)

    # Flatten the nested lists
    flattened_data = [item for sublist in json_data for item in sublist]
    return flattened_data


def generate_report(report_id):
    template_file = "template.html"
    output_dir = "out/" + report_id
    os.makedirs(output_dir, exist_ok=True)
    json_file_path = os.path.join(output_dir, f"data_{report_id}.json")
    data_list = load_and_flatten_json(json_file_path)
    data = pd.DataFrame(data_list)

    # Save reports and create HTML file
    save_reports_and_create_html(data, output_dir, template_file)


# generate_report(report_id)
