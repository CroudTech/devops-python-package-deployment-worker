```
Usage: cli.py [OPTIONS]

  Build all possible s3 paths for values files

Options:
  --namespace TEXT      The namespace for the release
  --chart TEXT          The name of the chart
  --app TEXT            The app name for the release  [required]
  --extrafiles TEXT     Extra file names to search for
  --extravalues TEXT    Full paths to extra values files
  --destination TEXT    The destination for downloaded values files
  --output [json|helm]  The source s3 bucket name  [required]
  --region TEXT         The target region
  --envname TEXT        The target environment
  --colour TEXT         The target colour
  --help                Show this message and exit.
```
