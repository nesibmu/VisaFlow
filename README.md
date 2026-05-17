# VisaFlow

VisaFlow is an AI operations agent for international-student bureaucracy. The goal is to turn scattered emails, PDFs, and form instructions into a clear action plan: deadlines, requested documents, next steps, and draft responses.

## Current scope
This repository reflects the current state of the project, which is focused on:
- defining the end-to-end user workflow
- building ingestion for emails, text files, and simple document content
- extracting deadlines, required documents, and action items
- converting extracted information into a structured task list
- generating draft email responses and concise next-step summaries

## Repository structure
- `visaflow/ingestion/` document loaders and normalization
- `visaflow/extraction/` deadline, document, and action-item extraction
- `visaflow/planning/` task graph / action-plan generation
- `visaflow/drafting/` email and summary drafting
- `data/samples/` sample administrative documents
- `tests/` lightweight unit tests

## Quick start
```bash
python -m visaflow.main data/samples/housing_email.txt
python -m visaflow.main data/samples/loan_request.txt
```

## What the current prototype does
The current prototype reads a document, extracts useful administrative signals, and returns:
1. detected deadlines
2. requested documents
3. action items
4. a prioritized task list
5. a draft reply email

## Next steps
- improve PDF parsing and OCR support
- add evidence linking back to source text spans
- add confidence scoring for extracted items
- support multi-document workflow state
- add a lightweight web interface
- test on more realistic university and immigration workflows
