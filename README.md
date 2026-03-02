SDECv2 is a recreation/upgrade of legacy SDEC. Replacing SDEC as of v2.0.0.

Before running:
- pip install -e .
- add the following to your .vscode/settings.json to prevent errors on SDECv2 internal imports
```
{
  "python.analysis.extraPaths": [
    "${workspaceFolder}/.."
  ]
}
```