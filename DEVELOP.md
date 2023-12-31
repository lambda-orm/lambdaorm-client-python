# Develop

## Initial commit

### Prerequisites

```shell
pip install commitizen
export PATH=$PATH:/home/flavio/.local/lib/python3.10/site-packages
commitizen init cz-conventional-changelog --save --save-exact
```

```bash
git init
git add .
```

## Release

```shell
git branch | sed -n -e 's/^\* \(.*\)/\1/p'

pip show lambdaorm | grep Version
```

### Manual Publish

Prerequisites:

```bash
pip install --upgrade twine requests_toolbelt urllib3
pip install requests_toolbelt==0.9.1 urllib3==1.26.8 twine==3.4.1
```

```bash
rm -rf build dist
python setup.py sdist
twine upload dist/*
```
