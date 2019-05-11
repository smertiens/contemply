import os
import shutil
import sys

root = os.path.dirname(os.path.abspath(__file__))

try:
    import contemply
    import contemply.cli as cli
except ModuleNotFoundError:
    sys.path.insert(0, (os.path.join(root, 'src')))

    import contemply
    import contemply.cli as cli


def clean_dist():
    shutil.rmtree(os.path.join(root, 'dist'))


def build_package():
    print('Building package...')
    print('Building for version {0}'.format(contemply.__version__))

    # Copy license file to it is included in the package
    shutil.copy(os.path.join(root, 'LICENSE'), os.path.join(root, 'src', 'contemply'))

    os.system('python3 setup.py sdist bdist_wheel')

    print('Checking files...')
    for file in [os.path.join(root, 'dist', 'contemply-{0}.tar.gz').format(contemply.__version__),
                 os.path.join(root, 'dist', 'contemply-{0}-py3-none-any.whl').format(contemply.__version__)]:

        if os.path.exists(file):
            print('{0} okay'.format(os.path.basename(file)))
        else:
            print('Missing file: {0}'.format(file))
            sys.exit(1)


def upload(dest='test'):
    if dest == 'test':
        # upload to testing environment
        ret = os.system('python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*')

        if ret != 0:
            print('Error while uploading.')

    elif dest == 'production':
        # upload to production environment
        ret = os.system('python3 -m twine upload dist/*')

        if ret != 0:
            print('Error while uploading.')

    else:
        print('Unknown destination')


def cleanup():
    print('cleaning up...')
    shutil.rmtree(os.path.join(root, 'build'))
    shutil.rmtree(os.path.join(root, 'src', 'contemply.egg-info'))
    os.unlink(os.path.join(root, 'src', 'contemply', 'LICENSE'))


if __name__ == '__main__':
    print('*** Publish to PyPi ***')

    if cli.prompt('Do you want to run tests before publishing?'):
        export = 'export PYTHONPATH="{0}:$PYTHONPATH"'.format(os.path.join(root, 'src'))
        ret = os.system('{0} && pytest tests --cov=contemply'.format(export))

        if ret != 0:
            print('pytest failed.')
            sys.exit()
        else:
            print('Tests okay.')

    clean_dist()
    build_package()

    print('Preparing upload...')
    production = cli.prompt('Is this a production release?', 'No')
    upload('production' if production else 'test')

    cleanup()
