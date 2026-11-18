# N8NATE Certificate Automation

An n8n automation project developed for the N8NATE competition in November 2025, where it secured First Place. N8NATE was part of a National Level Technical Symposium held at Meenakshi Sundararajan Engineering College in Chennai, Tamil Nadu. The project demonstrates how certificate requests can be collected, recorded in Google Sheets, personalised using an image template and delivered to recipients through Gmail.

## Project Overview

The automation manages the main steps involved in preparing and distributing completion certificates. It uses a form based workflow for new requests and a manual workflow for processing records already stored in Google Sheets.

## Problem Statement

Preparing certificates manually means entering recipient details on each certificate, saving the result and sending it to the right email address. It also takes extra effort to track which certificates are waiting to be processed and which have been sent.

## Solution

The project uses two n8n workflows to manage certificate generation and delivery.

The form workflow collects the certificate details and adds a record to Google Sheets. The manual workflow starts on demand and reads existing records. Each workflow checks the record status before processing, retrieves the certificate template, adds the recipient details to the image, sends the certificate through Gmail and updates the spreadsheet.

## Workflow Preview

![N8NATE certificate automation workflows](Assets/Workflow%20Screenshot.jpg)

### Certificate Template

![Certificate template](Assets/Certificate%20Template.jpg)

### Sample Certificate

![Sample certificate](Assets/Sample%20Certificate.jpg)

## Workflow Overview

### Form Workflow

1. **Form** collects the recipient name, email address, course and completion date.
2. **Store in Database** adds the submission to Google Sheets with a `Pending` status.
3. **Get row(s) in sheet** reads the spreadsheet records.
4. **IF** checks whether the record is pending.
5. The processing branch updates the record to `Processing`.
6. **Download Template Image** retrieves the certificate template. The Edit Image nodes add the recipient name, course and completion date.
7. **Send a message** sends the certificate through Gmail. The final Google Sheets node updates the record to `Sent`. The alternate branch leaves the existing status unchanged.

### Manual Workflow

1. **When clicking ‘Execute workflow’** starts the workflow.
2. **Get row(s) in sheet1** reads the spreadsheet records.
3. **If1** checks whether the record is pending.
4. The processing branch updates the record to `Processing`, retrieves the template and adds the recipient details.
5. **Send a message1** sends the certificate through Gmail. The final Google Sheets node updates the record to `Sent`. The alternate branch leaves the existing status unchanged.

## Tech Stack

- **n8n** for workflow automation.
- **n8n Form Trigger** for collecting certificate requests.
- **n8n Manual Trigger** for starting certificate processing.
- **Google Sheets** for storing recipient records and delivery status.
- **HTTP Request** for retrieving the certificate template image.
- **Edit Image** for placing recipient details on the certificate.
- **IF** for checking record status and controlling workflow paths.
- **Gmail** for sending the generated certificate as an email attachment.
- **n8n expressions** for passing recipient and certificate values between nodes.

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

## Getting Started

1. Create a Google Sheet with the columns `Participant Name`, `Participant Email`, `Course name`, `Completion Date`, `Status` and `Certificate Sent Date`.
2. Import `Sample Data/Sample Participants.csv` to add example records. Each sample address follows the `name@gmail.com` format and is illustrative. Replace it with a Gmail address you own before testing email delivery.
3. Add Google Sheets and Gmail credentials in n8n.
4. Import both workflow JSON files from the `Workflows` folder.
5. Select your Google Sheet and worksheet in each Google Sheets node.
6. Confirm that the HTTP Request nodes use the certificate template URL from this repository.
7. Check the name, course and date positions in the Edit Image nodes against the included certificate template.
8. Test with one record and an email address you control. Confirm that the certificate arrives as an attachment and that the spreadsheet status changes to `Sent`.

## Validation

Run the validation script from the project folder:

```bash
python "Tests/Validate Workflows.py"
```

The script checks the workflow JSON, required nodes, connections, status conditions, image handling, Gmail attachment mapping, sample data and project assets. It does not connect to Google Sheets or Gmail. A successful local check therefore does not confirm live email delivery.

## License

This project is licensed under the MIT License.
