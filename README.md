### Summary
SDECv2 is a recreation/upgrade of legacy SDEC. Replacing SDEC as of v2.0.0, with the following features:
- sensor dump
- dashboard dump
- preset management 
- flash extract

### Setup
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

### Testing

#### Run individual file test:
```
python -m Testing.<folder>.<filename>
```
Example: This line below runs test_engine_controller.py test
```
python -m Testing.EngineController.test_engine_controller
```