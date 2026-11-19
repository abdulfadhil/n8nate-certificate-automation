# N8NATE Certificate Automation

A certificate automation workflow built using n8n. It automates certificate creation and delivery through Google Sheets and Gmail.

The project was developed in November 2025 for N8NATE (Automation AI Agents Hackathon), where it secured First Place. N8NATE was part of EUPHORIA 2K25, a techno-cultural fest at Meenakshi Sundararajan Engineering College, Chennai.

## Project Overview

The project includes two workflows:

- **Form Workflow:** Collects new certificate requests and identifies each request with a unique Request ID.
- **Manual Workflow:** Processes existing `Pending` records in Google Sheets using their Request IDs.

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
2. Generates a unique Request ID and adds the request to Google Sheets with a `Pending` status.
3. Retrieves that request using its Request ID and checks its status.
4. Adds the participant's details to the certificate.
5. Sends the certificate through Gmail.
6. Updates the record to `Sent`.

[View Form Based Certificate Workflow](Workflows/Form%20Based%20Certificate%20Workflow.json)

### Manual Workflow

1. Reads existing records from Google Sheets.
2. Checks which records are `Pending`.
3. Uses each record's Request ID for status updates and adds participant details to the certificate.
4. Sends the certificate through Gmail.
5. Updates the record to `Sent`.

[View Manual Trigger Certificate Workflow](Workflows/Manual%20Trigger%20Certificate%20Workflow.json)

## Tech Stack

| Technology | Purpose |
|---|---|
| n8n | Workflow automation |
| Docker | Local n8n environment |
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

### 1. Run n8n locally with Docker

1. Install and open [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. Open PowerShell and run this command to create the n8n container:

```powershell
docker run -d --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n
```

3. Open http://localhost:5678 in your browser.
4. Complete the initial n8n setup.

If the n8n container already exists and is stopped, start it with:

```powershell
docker start n8n
```

### 2. Configure the workflows

1. Create a Google Sheet with these columns: Request ID, Participant Name, Participant Email, Course name, Completion Date, Status and Certificate Sent Date.
2. Add the example records from [Sample Participants.csv](Sample%20Data/Sample%20Participants.csv). Replace the sample email addresses with ones you control before testing.
3. Import both workflow JSON files from the [Workflows folder](Workflows/).
4. Configure your Google Sheets and Gmail credentials in n8n. Refer to the [Google credentials guide](https://docs.n8n.io/integrations/builtin/credentials/google/).
5. Select your Google Sheet and worksheet in the Google Sheets nodes.
6. Check the certificate template URL and image text positions.
7. Test the Form Workflow using its test URL. Publish it to receive submissions through its production URL.
8. Run the Manual Workflow using the Execute Workflow option.

For existing spreadsheets, add a Request ID column and give every existing record a unique, non-empty ID before running the updated Manual Workflow. For example, use EXISTING-001, EXISTING-002 and so on. Do not reuse IDs. New Form Workflow submissions generate their own Request IDs automatically.

Each user needs their own n8n instance, Google accounts and spreadsheet. The workflows use the shared certificate template in this repository.
## Testing

The workflows have been tested for certificate generation, Google Sheets updates and Gmail delivery.

Run the validation script from the project folder:

```bash
python "Tests/Validate Workflows.py"
```

The script checks project files and workflow configuration.

## License

This project is licensed under the [MIT License](LICENSE).
