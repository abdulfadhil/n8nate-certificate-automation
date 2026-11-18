#!/usr/bin/env python3
"""Run local structural checks for the N8NATE Certificate Automation project."""
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = {
    "form": ROOT / "Workflows" / "Form Based Certificate Workflow.json",
    "manual": ROOT / "Workflows" / "Manual Trigger Certificate Workflow.json",
}
EXPECTED = {
    "form": {
        "Form", "Store in Database", "Get row(s) in sheet", "IF",
        "Update row in sheet", "Download Template Image", "Edit Image Name",
        "Edit Image course", "Edit Image Date", "Send a message",
        "Update row in sheet (sent)", "Update row in sheet2",
    },
    "manual": {
        "When clicking ‘Execute workflow’", "Get row(s) in sheet1", "If1",
        "Update row in sheet4", "Download Template Image1", "Edit Image Name1",
        "Edit Image course1", "Edit Image Date1", "Send a message1",
        "Update row in sheet3", "Update row in sheet5",
    },
}

def check(condition, message, errors):
    if not condition:
        errors.append(message)

def main():
    errors = []
    required = [
        ROOT / "README.md", ROOT / "LICENSE", ROOT / ".gitignore",
        ROOT / "Assets" / "Certificate Template.jpg",
        ROOT / "Assets" / "Sample Certificate.jpg",
        ROOT / "Assets" / "Workflow Screenshot.jpg",
        ROOT / "Sample Data" / "Sample Participants.csv",
    ]
    for path in required:
        check(path.is_file() and path.stat().st_size > 0,
              f"Missing or empty file: {path.relative_to(ROOT)}", errors)

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    check("## Project Structure" in readme, "Project tree is missing", errors)
    check("## Tech Stack" in readme, "Tech Stack section is missing", errors)
    check("## Repository" not in readme and "github.com/abdulfadhil/" not in readme,
          "README should not link back to its own repository", errors)
    check("N8NATE Certificate Automation/" in readme, "Project folder name is inconsistent", errors)

    image_references = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", readme)
    check(len(image_references) == 3,
          "README must reference exactly three project images", errors)
    for reference in image_references:
        image_path = ROOT / reference.replace("%20", " ")
        check(image_path.is_file(),
              f"README image reference is missing: {reference}", errors)

    required_headings = [
        "## Project Overview",
        "## Problem Statement",
        "## Solution",
        "## Workflow Preview",
        "## Workflow Overview",
        "## Tech Stack",
        "## Project Structure",
        "## Getting Started",
        "## Testing",
        "## License",
    ]
    for heading in required_headings:
        check(heading in readme,
              f"README section is missing: {heading}", errors)

    for kind, path in WORKFLOWS.items():
        check(path.is_file(), f"Missing workflow: {path.name}", errors)
        if not path.is_file():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"Invalid JSON in {path.name}: {exc}")
            continue

        nodes = data.get("nodes", [])
        by_name = {node.get("name"): node for node in nodes}
        check(len(by_name) == len(nodes), f"{path.name}: duplicate node names", errors)
        check(EXPECTED[kind].issubset(by_name),
              f"{path.name}: missing expected screenshot nodes", errors)

        for source, outputs in data.get("connections", {}).items():
            check(source in by_name, f"{path.name}: unknown source node {source}", errors)
            for branches in outputs.values():
                for branch in branches:
                    for edge in branch:
                        check(edge.get("node") in by_name,
                              f"{path.name}: unknown target node {edge.get('node')}", errors)

        if_name = "IF" if kind == "form" else "If1"
        condition_list = by_name.get(if_name, {}).get("parameters", {}).get("conditions", {}).get("conditions", [])
        check(bool(condition_list), f"{path.name}: IF condition is missing", errors)
        if condition_list:
            condition = condition_list[0]
            check(condition.get("leftValue") == "={{ $json['Status'] }}" and
                  condition.get("rightValue") == "Pending" and
                  condition.get("operator", {}).get("operation") == "equals",
                  f"{path.name}: IF must check Status equals Pending", errors)

        if kind == "form":
            append_columns = by_name.get("Store in Database", {}).get("parameters", {}).get("columns", {})
            check(append_columns.get("value", {}).get("Request ID") == "={{ $execution.id }}",
                  "Form workflow must store the current execution ID as Request ID", errors)
            filter_values = by_name.get("Get row(s) in sheet", {}).get("parameters", {}).get("filtersUI", {}).get("values", [])
            check(len(filter_values) == 1, "Form workflow must have exactly one Request ID filter", errors)
            if len(filter_values) == 1:
                request_filter = filter_values[0]
                check(request_filter.get("lookupColumn") == "Request ID",
                      "Form workflow filter must use Request ID", errors)
                check(request_filter.get("lookupValue") == "={{ $execution.id }}",
                      "Form workflow filter must use the current execution ID", errors)
        else:
            manual_sheet = by_name.get("Get row(s) in sheet1", {}).get("parameters", {})
            check("filtersUI" not in manual_sheet, "Manual workflow must not filter pending records", errors)

        suffix = "" if kind == "form" else "1"
        sheet_node = "Get row(s) in sheet" if kind == "form" else "Get row(s) in sheet1"
        http = by_name.get(f"Download Template Image{suffix}", {}).get("parameters", {})
        response = http.get("options", {}).get("response", {}).get("response", {})
        check(response.get("responseFormat") == "file" and
              response.get("outputPropertyName") == "data",
              f"{path.name}: HTTP Request must return file data in 'data'", errors)

        for node_name, field in [
            (f"Edit Image Name{suffix}", "Participant Name"),
            (f"Edit Image course{suffix}", "Course name"),
            (f"Edit Image Date{suffix}", "Completion Date"),
        ]:
            params = by_name.get(node_name, {}).get("parameters", {})
            check(params.get("dataPropertyName") == "data",
                  f"{path.name}: {node_name} must use binary property 'data'", errors)
            text = params.get("text", "")
            check(field in text and sheet_node in text,
                  f"{path.name}: {node_name} is missing its sheet field mapping", errors)

        gmail = by_name.get("Send a message" + suffix, {}).get("parameters", {})
        attachments = gmail.get("options", {}).get("attachmentsUi", {}).get("attachmentsBinary", [])
        check(any(item.get("property") == "data" for item in attachments),
              f"{path.name}: Gmail attachment must use binary property 'data'", errors)
        check(sheet_node in gmail.get("sendTo", ""),
              f"{path.name}: Gmail recipient mapping is missing", errors)

        processing_name = "Update row in sheet" if kind == "form" else "Update row in sheet4"
        sent_name = "Update row in sheet (sent)" if kind == "form" else "Update row in sheet3"
        alternate_name = "Update row in sheet2" if kind == "form" else "Update row in sheet5"

        for node_name, status in ((processing_name, "Processing"), (sent_name, "Sent")):
            params = by_name.get(node_name, {}).get("parameters", {}).get("columns", {})
            values = params.get("value", {})
            matching = params.get("matchingColumns", [])
            check(values.get("Status") == status,
                  f"{path.name}: {node_name} must set Status to {status}", errors)
            check("Request ID" in values and matching == ["Request ID"],
                  f"{path.name}: {node_name} must match rows by Request ID", errors)
            check(values.get("Request ID") == f"={{{{ $('{sheet_node}').item.json['Request ID'] }}}}",
                  f"{path.name}: {node_name} must use the current row's Request ID", errors)
            if status == "Sent":
                check(values.get("Certificate Sent Date") == "={{ $now.toISO() }}",
                      f"{path.name}: {node_name} must record the certificate sent date",
                      errors)

        alternate = by_name.get(alternate_name, {}).get("parameters", {}).get("columns", {})
        alternate_values = alternate.get("value", {})
        alternate_match = alternate.get("matchingColumns", [])
        check(alternate_values.get("Status") == f"={{{{ $('{sheet_node}').item.json['Status'] }}}}",
              f"{path.name}: alternate branch must preserve existing status", errors)
        check("Request ID" in alternate_values and alternate_match == ["Request ID"],
              f"{path.name}: alternate branch must match rows by Request ID", errors)
        check(alternate_values.get("Request ID") == f"={{{{ $('{sheet_node}').item.json['Request ID'] }}}}",
              f"{path.name}: alternate branch must use the current row's Request ID", errors)

    csv_path = ROOT / "Sample Data" / "Sample Participants.csv"
    if csv_path.is_file():
        with csv_path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        expected_columns = {"Request ID", "Participant Name", "Participant Email",
                            "Course name", "Completion Date", "Status",
                            "Certificate Sent Date"}
        check(bool(rows), "Sample participant data is empty", errors)
        check(expected_columns.issubset(rows[0].keys()) if rows else False,
              "Sample participant data is missing required columns", errors)
        request_ids = [row.get("Request ID", "").strip() for row in rows]
        check(all(request_ids), "Every sample record must have a Request ID", errors)
        check(len(request_ids) == len(set(request_ids)),
              "Sample Request IDs must be unique", errors)
        emails = [row["Participant Email"].strip().lower() for row in rows]
        check(all(emails), "Every sample record must have a participant email", errors)
        check(len(emails) == len(set(emails)),
              "Sample participant email addresses must be unique", errors)

    for path in ROOT.rglob("*"):
        if path.is_file() and path != Path(__file__) and path.suffix.lower() in {".md", ".txt", ".json", ".py", ".csv"}:
            content = path.read_text(encoding="utf-8", errors="replace").lower()
            excluded_a = "grey" + " " + "atoms"
            excluded_b = "dhar" + "un"
            check(excluded_a not in content and excluded_b not in content,
                  f"{path.relative_to(ROOT)} contains a name excluded from this repository", errors)

    if errors:
        print(f"FAIL: {len(errors)} check(s)")
        for error in errors:
            print(f" - {error}")
        return 1

    print("PASS: project files, README, project tree, Tech Stack, JSON syntax, workflow nodes,")
    print("      connections, IF rules, status updates, image mapping, Gmail attachment mapping,")
    print("      timestamp mapping, README links, sample data, Request ID filters, unique sample IDs and excluded-name scan.")
    print("NOTE: live n8n, Google Sheets and Gmail execution are not tested by this script.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
