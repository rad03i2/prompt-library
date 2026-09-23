# Security Policy

## Supported version
The latest version on `main` receives security fixes.

## Security model
Prompt Library is local-first and performs no network requests. Prompt files are plain JSON and templates are substituted as text; values are not executed as code. Prompt names are restricted to safe slugs to prevent path traversal.

Treat prompts and rendered output as untrusted text when passing them to agents or tools. This project does not make an LLM safe and does not authorize tool actions.

## Reporting
Please report vulnerabilities privately through GitHub's security reporting features when available. Do not include real secrets in reports.
