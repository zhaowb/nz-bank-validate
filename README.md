# NZ Bank validator
This package validates account numbers for all New Zealand banks, based on chapter "8. Bank account number validation" in ["2020 Resident Withholding
Tax (RWT) and Non-Resident Withholding Tax (NRWT) - Software Requirements Specification
For the year ending 31 March 2020"](https://www.ird.govt.nz/-/media/project/ir/home/documents/income-tax/withholding-taxes/rwt-nrwt-withholding-tax-certificate/2020-rwt-and-nrwt-certificate-filing-specification.pdf) 

```
from nz_bank_validate import nz_bank_validate

nz_bank_validate(*'08-6523-1954512-001'.split('-'))
```

If validate succeeded, the function returns True.

If validate failed, the function raises ValueError('invalid').

Or use option `return_false_on_fail` to explicitly indicate return False when invalid:
```
nz_bank_validate(*'08-6523-1954512-001'.split('-'), return_false_on_fail=False)
```
