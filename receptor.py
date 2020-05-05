# receptor Reiable UDP
from helper import *
from argparse import ArgumentParser
import socket
import logging

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

def main():
    parser = ArgumentParser(usage=__file__ + ' '
                                             '-p/--port PORT'
                                             '-f/--fisier FILE_PATH',
                            description='Reliable UDP Receptor')

    parser.add_argument('-p', '--port',
                        dest='port',
                        default='10000',
                        help='Portul pe care sa porneasca receptorul pentru a primi mesaje')

    parser.add_argument('-f', '--fisier',
                        dest='fisier',
                        help='Calea catre fisierul in care se vor scrie octetii primiti')

    # Parse arguments
    args = vars(parser.parse_args())
    port = args['port']
    fisier = args['fisier']

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)

    adresa = '0.0.0.0'
    server_address = (adresa, port)
    sock.bind(server_address)
    logging.info("Serverul a pornit pe %s si portnul portul %d", adresa, port)

    f = open("my_file", "r+b")

    while True:
        logging.info('Asteptam mesaje...')
        data, address = sock.recvfrom(MAX_SEGMENT)
        header = data[:8]
        mesaj = data[8:]
        sequence_number, checksum, flags = parse_header_emitator(header)   #parsam headerul de la emitator

        if !verifica_checksum(checksum):    # verificam checksum
            continue

        if flags & 0b100 or flags & 0b001:
            ack_nr = sequence_number + 1
        elif flags & 0b010:
            ack_nr = sequence_number

        try:
            f.write(mesaj)
        except IOError:
            f.close()

        '''        
        3. trimitem confirmari cu ack = seq_nr+1 daca mesajul e de tip S sau F
                               cu ack = seq_nr daca mesajul e de tip P
        4. scriem intr-un fisier octetii primiti
        5. verificam la sfarsit ca fisierul este la fel cu cel trimis de emitator
        '''

        checksum = 0
        window = random.randint(1, 5)

        octeti = struct.pack('!LHH', ack_nr, checksum, window)
        sock.sendto(emitator, octeti)


if __name__ == '__main__':
    main()

