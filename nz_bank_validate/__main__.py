from . import nz_bank_validate, max_length
import sys
def main():
    if len(sys.argv) == 2:
        account_number = sys.argv[-1]
        if '-' in account_number:
            parts = account_number.split('-')
            if len(parts) != 4:
                print('00-0000-00000000-000 format is expected if - is in number')
                sys.exit(1)
            bank, branch, base, suffix = parts
        else:
            bank, rest = account_number[:max_length['bank']], account_number[max_length['bank']:]
            branch, rest = rest[:max_length['branch']], rest[max_length['branch']:]
            base, rest = rest[:max_length['base']], rest[max_length['base']:]
            suffix = rest
    elif len(sys.argv) == 5:
        bank, branch, base, suffix = sys.argv[1:]
    else:
        print('python -m nz_bank_validate account_number')
        print('    account_number format allowed:')
        print('    001111222222223333')
        print('    00-1111-22222222-3333')
        print('    00 1111 22222222 3333')
        sys.exit(1)
    if nz_bank_validate(bank, branch, base, suffix, return_false_on_fail=True):
        print(f'{bank}-{branch}-{base}-{suffix} is valid')
        sys.exit(0)
    else:
        print(f'{bank}-{branch}-{base}-{suffix} is invalid')
        sys.exit(1)

if __name__ == '__main__':
    main()
