# see https://packaging.python.org/tutorials/packaging-projects/
#

watch: export PYTHONPATH=.
watch:
	ptw tests/ nz_bank_validate -- -vv

watch/%: export PYTHONPATH=.
watch/%:
	ptw tests/$* nz_bank_validate -- -vv

test: export PYTHONPATH=.
test:
	pytest tests/ -vv

test/%: export PYTHONPATH=.
test/%:
	pytest tests/$* -vv

timeit:
	@echo Algo A
	python -m timeit -s 'from nz_bank_validate import nz_bank_validate' 'nz_bank_validate("01", "902", "0068389", "00")'
	python -m timeit -s 'from nz_bank_validate import nz_bank_validate2' 'nz_bank_validate2("01", "902", "0068389", "00")'
	python -m timeit -s 'from nz_bank_validate import nz_bank_validate3' 'nz_bank_validate3("01", "902", "0068389", "00")'
	@echo Algo D
	python -m timeit -s 'from nz_bank_validate import nz_bank_validate' 'nz_bank_validate("08", "6523", "1954512", "001")'
	python -m timeit -s 'from nz_bank_validate import nz_bank_validate2' 'nz_bank_validate2("08", "6523", "1954512", "001")'
	python -m timeit -s 'from nz_bank_validate import nz_bank_validate3' 'nz_bank_validate3("08", "6523", "1954512", "001")'
	@echo Algo G
	python -m timeit -s 'from nz_bank_validate import nz_bank_validate' 'nz_bank_validate("26", "2600", "0320871", "032")'
	python -m timeit -s 'from nz_bank_validate import nz_bank_validate2' 'nz_bank_validate2("26", "2600", "0320871", "032")'
	python -m timeit -s 'from nz_bank_validate import nz_bank_validate3' 'nz_bank_validate3("26", "2600", "0320871", "032")'

develop:
	python3 setup.py develop

build-dist:
	rm -rf build/ dist/ *.egg-info/
	python3 setup.py sdist bdist_wheel

publish-test:
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

publish:
	python3 -m twine upload dist/*

