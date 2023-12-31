"""Tasks for building and publishing the package."""
import os
import subprocess
from invoke import task, Collection

def get_current_branch():
    """Get the current branch name."""
    try:
        return subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], universal_newlines=True).strip()
    except subprocess.CalledProcessError:
        return None

ns = Collection()
ns.configure({'run': {'executable': 'python3'}})

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
    current_branch = get_current_branch()
    version = os.getenv('VERSION')
    cmd= f"""git add . && git commit -m "chore(release): "{version}" && git push && git push --tags
				  &&  git checkout -b release/"{version}" && git push --set-upstream origin release/"{version}"
				  &&  git checkout main && git merge release/"{version}" -m "chore(release): release "{version}" " && git push
				  &&  git checkout "{current_branch}" && git merge release/"{version}" -m "chore(release): release "{version}"" && git push
				  &&  git branch -D release/"{version}" """
    ctx.run(cmd)

@task(test)
def publish(ctx):
    """Publish the package to PyPI."""
    username = os.getenv('PYPI_USERNAME')
    password = os.getenv('PYPI_PASSWORD')
    if not username or not password:
        raise ValueError("PyPI credentials not found in environment variables.")

    # Aquí utiliza las credenciales en tu comando de publicación
    cmd = f'twine upload --username "{username}" --password "{password}" dist/*'
    ctx.run(cmd)
