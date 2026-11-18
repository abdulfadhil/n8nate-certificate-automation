# N8NATE Certificate Automation

An n8n project developed for the N8NATE competition in November 2025, where it secured First Place. The competition was part of a National Level Technical Symposium at Meenakshi Sundararajan Engineering College, Chennai, Tamil Nadu.

The project automates certificate creation and delivery using Google Sheets and Gmail.

## Project Overview

The project includes two workflows:

- **Form Workflow:** Collects new certificate requests.
- **Manual Workflow:** Processes existing records in Google Sheets.

## Problem Statement

Creating certificates manually takes time. Participant details must be added to each certificate, emails must be sent, and delivery status must be tracked.

## Solution

The workflows collect or read participant details, add them to a certificate template, send the certificate through Gmail, and update the record in Google Sheets.

## Workflow Preview

[![N8NATE Workflow Screenshot](Assets/Workflow%20Screenshot.jpg)](Assets/Workflow%20Screenshot.jpg)

## Certificate Template

[![Certificate Template](Assets/Certificate%20Template.jpg)](Assets/Certificate%20Template.jpg)

## Sample Certificate

[![Sample Certificate](Assets/Sample%20Certificate.jpg)](Assets/Sample%20Certificate.jpg)

## Workflow Overview

### Form Workflow

1. Collects the participant's name, email, course and completion date.
2. Adds the details to Google Sheets with a `Pending` status.
3. Checks the record status.
4. Adds the participant's details to the certificate.
5. Sends the certificate through Gmail.
6. Updates the record to `Sent`.

[View Form Based Certificate Workflow](Workflows/Form%20Based%20Certificate%20Workflow.json)

### Manual Workflow

1. Reads existing records from Google Sheets.
2. Checks which records are `Pending`.
3. Adds participant details to the certificate.
4. Sends the certificate through Gmail.
5. Updates the record to `Sent`.

[View Manual Trigger Certificate Workflow](Workflows/Manual%20Trigger%20Certificate%20Workflow.json)

## Tech Stack

| Technology | Purpose |
|---|---|
| n8n | Workflow automation |
| Google Sheets | Participant data and status tracking |
| Gmail | Certificate email delivery |
| Python | Local project validation |

## Project Structure

```text
N8NATE Certificate Automation/
├── README.md
├── LICENSE
├── .gitignore
├── Assets/
│   ├── Certificate Template.jpg
│   ├── Sample Certificate.jpg
│   └── Workflow Screenshot.jpg
├── Sample Data/
│   └── Sample Participants.csv
├── Tests/
│   └── Validate Workflows.py
└── Workflows/
    ├── Form Based Certificate Workflow.json
    └── Manual Trigger Certificate Workflow.json
```

**Project folders:** [Assets](Assets/) · [Sample Data](Sample%20Data/) · [Tests](Tests/) · [Workflows](Workflows/)

## Getting Started

1. Create a Google Sheet with these columns: `Participant Name`, `Participant Email`, `Course name`, `Completion Date`, `Status` and `Certificate Sent Date`.
2. Add the example records from [Sample Participants.csv](Sample%20Data/Sample%20Participants.csv). Replace the sample email addresses with ones you control before testing.
3. Add your Google Sheets and Gmail credentials in n8n.
4. Import both workflow files from the [Workflows folder](Workflows/).
5. Select your Google Sheet and worksheet in the Google Sheets nodes.
6. Check the certificate template URL and image text positions.
7. Test with one participant and confirm that the email and spreadsheet update work correctly.

## Testing

Run this command from the project folder:

```bash
python "Tests/Validate Workflows.py"
```

The script checks project files and workflow configuration. Both workflows were also manually tested, including certificate generation, Google Sheets updates, and Gmail delivery.

## License

This project is licensed under the [MIT License](LICENSE).
