del /s/q dist\* 
python setup.py bdist_wheel
python setup.py sdist
twine upload dist/*