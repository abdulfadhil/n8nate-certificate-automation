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
|-- README.md
|-- LICENSE
|-- .gitignore
|-- Assets/
|   |-- Certificate Template.jpg
|   |-- Sample Certificate.jpg
|   |-- Workflow Screenshot.jpg
|-- Sample Data/
|   |-- Sample Participants.csv
|-- Tests/
|   |-- Validate Workflows.py
|-- Workflows/
|   |-- Form Based Certificate Workflow.json
|   |-- Manual Trigger Certificate Workflow.json
```

**Project folders:** [Assets](Assets/) | [Sample Data](Sample%20Data/) | [Tests](Tests/) | [Workflows](Workflows/)

## Getting Started

1. Install and start n8n on your computer using the [official installation guide](https://docs.n8n.io/hosting/installation/).
2. Open the local n8n address shown by your installation. The default address for a local setup is `http://localhost:5678`.
3. Create a Google Sheet with these columns: `Participant Name`, `Participant Email`, `Course name`, `Completion Date`, `Status` and `Certificate Sent Date`.
4. Add the example records from [Sample Participants.csv](Sample%20Data/Sample%20Participants.csv). Replace the sample email addresses with ones you control before testing.
5. Import both workflow files from the [Workflows folder](Workflows/).
6. Configure your own Google Sheets and Gmail credentials in n8n. Refer to the [Google credentials guide](https://docs.n8n.io/integrations/builtin/credentials/google/).
7. Select your Google Sheet and worksheet in the Google Sheets nodes.
8. Check the certificate template URL and image text positions.
9. Test the Form Workflow using its test URL. Publish the workflow to receive submissions through its production URL.
10. Run the Manual Workflow using the Execute Workflow option.

Each user needs their own n8n instance, Google accounts and spreadsheet. The workflows use the shared certificate template in this repository.

## Testing

Run this command from the project folder:

```bash
python "Tests/Validate Workflows.py"
```

The script checks project files and workflow configuration. It does not execute the workflows or test live Google Sheets and Gmail connections.

Both workflows were also manually tested, including certificate generation, Google Sheets updates and Gmail delivery.

## License

This project is licensed under the [MIT License](LICENSE).
