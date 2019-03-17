
cd `dirname $0`
cd ../src

test -f ./VERSION || (echo "file VERSION containing current version is needed" && exit 1)

python3 setup.py sdist bdist_wheel

ls -1

# -u $PYPIUSERNAME -p $PYPIPASSWORD

python3 -m twine upload  dist/*

# git clean -fd
