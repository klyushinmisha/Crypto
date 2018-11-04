from crypto import Encrypter, Decrypter


def main():
    e = Encrypter(2, 1)
    d = Decrypter(2, 1, e.gamma)

    value = e.encrypt("This is useless string".encode('ascii'))
    b = d.decrypt(value, e.gamma)
    print(b.decode('ascii'))


if __name__ == '__main__':
    main()
