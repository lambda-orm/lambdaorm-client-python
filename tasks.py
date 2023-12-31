"""Tasks for building and publishing the package."""
import os
from invoke import task, Collection

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
def publish(ctx):
    """Publish the package to PyPI."""
    username = os.getenv('PYPI_USERNAME')
    password = os.getenv('PYPI_PASSWORD')
    if not username or not password:
        raise ValueError("PyPI credentials not found in environment variables.")

    # Aquí utiliza las credenciales en tu comando de publicación
    cmd = f'twine upload --username "{username}" --password "{password}" dist/*'
    ctx.run(cmd)
