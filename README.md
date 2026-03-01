SDECv2 is an in-progress recreation/upgrade of legacy SDEC.

Before running:
- pip install -e .
- add the following to your .vscode/settings.json to prevent errors on SDECv2 internal imports
```
{
  "python.analysis.extraPaths": [
    "${workspaceFolder}"
  ]
}
```