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


# Function to generate report f by user
def report_f_by_user(data):
    # Group by assignee and type
    grouped = data.groupby(["assignee", "type"])

    # Initialize an empty dictionary to store the HTML tables
    report_f_by_user_html = {}

    # Iterate over each group
    for (assignee, type_), group in grouped:
        # Filter out relevant columns and convert 'key' to hyperlink
        filtered_group = group[
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
        filtered_group["key"] = filtered_group.apply(
            lambda x: f'<a href="{x["link"]}" target="_blank">{x["key"]}</a>', axis=1
        )

        # Convert to HTML table with assignee as heading
        table_html = f"<h3>{assignee}</h3>\n"
        table_html += filtered_group.drop(columns=["link"]).to_html(
            index=False, classes="table table-sortable", escape=False
        )

        # Save the HTML table for this assignee and type
        report_f_by_user_html[(assignee, type_)] = table_html

    return report_f_by_user_html


# Function to generate report f by type
def report_f_by_type(data):
    # Group by type
    grouped = data.groupby("type")

    # Initialize an empty dictionary to store the HTML tables
    report_f_by_type_html = {}

    # Iterate over each group
    for type_, group in grouped:
        # Filter out relevant columns and convert 'key' to hyperlink
        filtered_group = group[
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
        filtered_group["key"] = filtered_group.apply(
            lambda x: f'<a href="{x["link"]}" target="_blank">{x["key"]}</a>', axis=1
        )

        # Convert to HTML table with type as heading
        table_html = f"<h3>{type_}</h3>\n"
        table_html += filtered_group.drop(columns=["link"]).to_html(
            index=False, classes="table table-sortable", escape=False
        )

        # Save the HTML table for this type
        report_f_by_type_html[type_] = table_html

    return report_f_by_type_html


# Function to save reports to CSV files and create HTML content
def save_reports_and_create_html(data, output_dir, template_file):
    # Generate reports
    report_a = report_issue_counts(data)
    report_b = report_user_issue_counts(data)
    report_c = report_user_story_status_counts(data)
    report_d = report_sub_task_status_counts(data)
    report_e = report_latest_updates(data)
    report_f_user = report_f_by_user(data)
    report_f_type = report_f_by_type(data)

    # Convert reports to HTML tables
    report_a_html = report_a.rename(columns=str.capitalize).to_html(
        index=False, classes="table table-sortable", escape=False
    )
    report_b_html = report_b.rename(columns=str.capitalize).to_html(
        index=False, classes="table table-sortable", escape=False
    )
    report_c_html = report_c.rename(columns=str.capitalize).to_html(
        index=False, classes="table table-sortable", escape=False
    )
    report_d_html = report_d.rename(columns=str.capitalize).to_html(
        index=False, classes="table table-sortable", escape=False
    )
    report_e_html = report_e.rename(columns=str.capitalize).to_html(
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
        report_f_by_user="\n".join(report_f_user.values()),
        report_f_by_type="\n".join(report_f_type.values()),
    )

    # Save HTML content to file
    with open("index.html", "w") as file:
        file.write(html_content)

    print("Reports have been saved to index.html.")


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
