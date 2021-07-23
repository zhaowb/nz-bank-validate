"""Validate NZ bank account number.
Refer to document: [RWT and NRWT Certificates / 2020 / Version 1.0](https://www.ird.govt.nz/-/media/project/ir/home/documents/income-tax/withholding-taxes/rwt-nrwt-withholding-tax-certificate/2020-rwt-and-nrwt-certificate-filing-specification.pdf) charpter 8. Bank account number validation
"""

__all__ = ['nz_bank_validate']
max_length = {
    'bank': 2,
    'branch': 4,
    'base': 8,
    'suffix': 4,
}

# The order of following data seems strange because it's copy/pasted from pdf file then manually modified
branch_numbers = {
    '01': [('0001', '0999'), ('1100', '1199'), ('1800', '1899')],
    '20': [('4100', '4199')],
    '02': [('0001', '0999'), ('1200', '1299')],
    '21': [('4800', '4899')],
    '03': [('0001', '0999'), ('1300', '1399'), ('1500', '1599'), ('1700', '1799'), ('1900', '1999'), ('7350', '7399')],
    '22': [('4000', '4049')],
    '04': [('2020', '2024')],
    '06': [('0001', '0999'), ('1400', '1499')],
    '23': [('3700', '3799')],
    '08': [('6500', '6599')],
    '24': [('4300', '4349')],
    '09': [('0000', '0000')],
    '25': [('2500', '2599')],
    '10': [('5165', '5169')],
    '26': [('2600', '2699')],
    '11': [('5000', '6499'), ('6600', '8999')],
    '12': [('3000', '3299'), ('3400', '3499'), ('3600', '3699')],
    '27': [('3800', '3849')],
    '13': [('4900', '4999')],
    '28': [('2100', '2149')],
    '14': [('4700', '4799')],
    '29': [('2150', '2299')],
    '15': [('3900', '3999')],
    '30': [('2900', '2949')],
    '16': [('4400', '4499')],
    '31': [('2800', '2849')],
    '17': [('3300', '3399')],
    '33': [('6700', '6799')],
    '18': [('3500', '3599')],
    '35': [('2400', '2499')],
    '19': [('4600', '4649')],
    '38': [('9000', '9499')],
}

algorithms = {
    '01': 'See note',
    '20': 'See note',
    '02': 'See note',
    '21': 'See note',
    '03': 'See note',
    '22': 'See note',
    '04': 'See note',  # possible missing in document
    '06': 'See note',
    '23': 'See note',
    '08': 'D',
    '24': 'See note',
    '09': 'E',
    '25': 'F',
    '10': 'See note',
    '26': 'G',
    '11': 'See note',
    '12': 'See note',
    '27': 'See note',
    '13': 'See note',
    '28': 'G',
    '14': 'See note',
    '29': 'G',
    '15': 'See note',
    '30': 'See note',
    '16': 'See note',
    '31': 'X',
    '17': 'See note',
    '33': 'F',
    '18': 'See note',
    '35': 'See note',
    '19': 'See note',
    '38': 'See note',
}

weights = {
    # Algorithm
    # .....Bank
    # .....v.....Branch
    # .....v.....v...........Account Base
    # .....v.....v...........v........................Suffix
    # .....v.....v...........v........................v............Modulo
    'A': ((0, 0, 6, 3, 7, 9, 0, 0, 10, 5, 8, 4, 2, 1, 0, 0, 0, 0), 11),
    'B': ((0, 0, 0, 0, 0, 0, 0, 0, 10, 5, 8, 4, 2, 1, 0, 0, 0, 0), 11),
    'C': ((3, 7, 0, 0, 0, 0, 9, 1, 10, 5, 3, 4, 2, 1, 0, 0, 0, 0), 11),
    'D': ((0, 0, 0, 0, 0, 0, 0, 7,  6, 5, 4, 3, 2, 1, 0, 0, 0, 0), 11),
    'E': ((0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 5, 4, 3, 2, 0, 0, 0, 1), 11),
    'F': ((0, 0, 0, 0, 0, 0, 0, 1,  7, 3, 1, 7, 3, 1, 0, 0, 0, 0), 10),
    'G': ((0, 0, 0, 0, 0, 0, 0, 1,  3, 7, 1, 3, 7, 1, 0, 3, 7, 1), 10),
    'X': ((0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0, 0, 0, 0, 0), 1),
}


def check_branch_number(bank, branch):
    for a, b in branch_numbers.get(bank) or []:
        if a <= branch <= b:
            return True
    return False


def get_algorithm(bank, branch, base, suffix):
    definition = algorithms.get(bank)
    if definition == 'See note':
        return 'A' if base < '00990000' else 'B'
    return definition


def multiply(algorithm: str, digit: int, factor: int) -> int:
    result = digit * factor
    if algorithm in ('E', 'G'):
        # See 'Example 3' in pdf, page 16
        result = (result // 10) + (result % 10)
        result = (result // 10) + (result % 10)
    return result


def nz_bank_validate(bank: str, branch: str, base: str, suffix: str, *, return_false_on_fail=False) -> bool:
    """Validate New Zealand bank account number, return True if valid, raise ValueError('invalid') if invalid
    or return False if invalid and option return_false_on_fail=True
    Example:
    ``nz_bank_validate(*'01-902-0068389-00'.split('-'))``
    or
    ``nz_bank_validate('01', '902', '0068389', '00')``
    """
    bank = bank.zfill(max_length['bank'])
    branch = branch.zfill(max_length['branch'])
    base = base.zfill(max_length['base'])
    suffix = suffix.zfill(max_length['suffix'])
    for value, length in zip([bank, branch, base, suffix], max_length.values()):
        if len(value) != length:
            if return_false_on_fail:
                return False
            raise ValueError('invalid')
    if not check_branch_number(bank, branch):
        if return_false_on_fail:
            return False
        raise ValueError('invalid')
    algo = get_algorithm(bank, branch, base, suffix)
    if algo not in weights:
        if return_false_on_fail:
            return False
        raise ValueError('invalid')
    weight, modulo = weights[algo]
    number = ''.join((bank, branch, base, suffix))
    sum_weight = sum(
        multiply(algo, int(digit), factor)
        for digit, factor in zip(number, weight)
    )
    if (sum_weight % modulo) != 0:
        if return_false_on_fail:
            return False
        raise ValueError('invalid')
    return True
