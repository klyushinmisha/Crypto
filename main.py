from crypto import Encrypter, Decrypter
import sys


def load_args():
    args = dict()
    for word in sys.argv[1:]:
        k, v = word.split('=')
        args[k[1:]] = v
    return args


def main():
    args = load_args()

    with open(args["i"], 'rb') as in_file:
        b = in_file.read()

    chunk_size = int(args["cs"])
    bias = int(args["b"])

    with open(args["o"], 'wb') as out_file:
        if 'd' in args:
            key = int(args['d'])
            d = Decrypter(chunk_size, bias, key)
            b_seq = d.decrypt(b, key)
            print(b_seq.decode('ascii'))
            out_file.write(b_seq)
        else:
            e = Encrypter(chunk_size, bias)
            b_seq = e.encrypt("This is useless string".encode('ascii'))
            print("Your key is {0}".format(e.gamma))
            out_file.write(b_seq)


if __name__ == '__main__':
    main()
