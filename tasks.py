"""Tasks for building and publishing the package."""
import os
import re
from invoke import task, Collection
ns = Collection()

ns.configure({'run': {'executable': 'python3'}})

def get_version():
    """Get the package version from the source code."""
    with open('setup.py', 'r', encoding='utf8') as archivo_setup:
        contenido = archivo_setup.read()
    version = re.search(r"version=['\"]([^'\"]+)['\"]", contenido)
    return version.group(1)

@task
def clean(ctx):
    """Clean up build and distribution artifacts."""
    ctx.run("rm -rf build dist")

@task(clean)
def build(ctx):
    """Build the distribution package."""
    ctx.run("python3 setup.py sdist bdist_wheel")

@task(build)
def test(ctx):
    """Run tests."""
    ctx.run("pytest")

@task(test)
def release(ctx):
    """Package and upload a release."""
    version = get_version()
    resultado = ctx.run("git branch | sed -n -e 's/^\* \(.*\)/\1/p'", hide=True)
    current_branch = resultado.stdout.strip()
    cmd = (
        f"git add . && git commit -m 'chore(release): {version}' && git push && git push --tags"
        f" && git checkout -b release/{version} && git push --set-upstream origin release/{version}"
        f" && git checkout main && git merge release/{version} -m 'chore(release): release {version}' && git push"
        f" && git checkout {current_branch} && git merge release/{version} -m 'chore(release): release {version}' && git push"
        f" && git branch -D release/{version}"
    )
    ctx.run(cmd)

@task(test)
def publish(ctx):
    """Publish the package to PyPI."""
    username = os.getenv('PYPI_USERNAME')
    password = os.getenv('PYPI_PASSWORD')
    if not username or not password:
        raise ValueError("PyPI credentials not found in environment variables.")
    cmd = f'twine upload --username "{username}" --password "{password}" dist/*'
    ctx.run(cmd)
