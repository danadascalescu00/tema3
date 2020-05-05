# emitator Reliable UDP
from helper import *
from argparse import ArgumentParser
import socket
import logging
import sys

# Variables declarations
initial_sequence_nr = random.randint(0, MAX_UINT32)

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

#cerere de conectare
def connect(sock, adresa_receptor):
    '''
    Functie care initializeaza conexiunea cu receptorul.
    Returneaza ack_nr de la receptor si window
    '''
    seq_nr = initial_sequence_nr  
    flags = 'S'
    checksum = 0
    octeti_header_fara_checksum = create_header_emitator(seq_nr, flags, checksum)
    
    mesaj = octeti_header_fara_checksum
    checksum = calculeaza_checksum(mesaj)
    octeti_header_cu_checksum = create_header_emitator(seq_nr, flags, checksum)

    mesaj = octeti_header_cu_checksum
    
    #   in cazul in care numarul de secventa + numarul de octeti depaseste numarul maxim
    while seq_nr + len(mesaj) >= MAX_UINT32:
        initial_sequence_nr = random.randint(0, MAX_UINT32)
        seq_nr = initial_sequence_nr
        
    seq_nr = seq_nr + len(mesaj) # sequence number este incrementat in functie de cati octeti trimite emitatorul
        
    sock.sendto(mesaj, adresa_receptor)
    
    while True:
        try:
            data, server = sock.recvfrom(MAX_SEGMENT)
            if data:
                break
        except sock.timeout as e:
            sock.settimeout(10)
            continue

    if verifica_checksum(data) is False:
        #daca checksum nu e ok, mesajul de la receptor trebuie ignorat
        return -1, -1
    
    ack_nr, checksum, window = parse_header_receptor(data)

    logging.info('Ack Nr: "%d"', ack_nr)
    logging.info('Checksum: "%d"', checksum)
    logging.info('Window: "%d"', window)

    return ack_nr, window

# cerere de finalizare
def finalize(sock, adresa_receptor, seq_nr):
    '''
    Functie care trimite mesajul de finalizare
    cu seq_nr dat ca parametru.
    '''
    # TO DO:
    # folositi pasii de la connect() pentru a construi headerul
    # valorile de checksum si pentru a verifica primirea mesajului a avut loc
    flags = 'F'
    checksum = 0
    octeti_header_fara_checksum = create_header_emitator(seq_nr, flags, checksum)
    
    mesaj = octeti_header_fara_checksum
    checksum = calculeaza_checksum(mesaj)
    octeti_header_cu_checksum = create_header_emitator(seq_nr, flags, checksum)

    mesaj = octeti_header_cu_checksum

    sock.sendto(mesaj, adresa_receptor)

    while True:
        try:
            data, server = sock.recvfrom(MAX_SEGMENT)
            if data:
                break
        except sock.timeout as e:
            sock.settimeout(10)
            continue

    if verifica_checksum(data) is False:
        #daca checksum nu e ok, mesajul de la receptor trebuie ignorat
        return -1

    return 0


#mesaj cu date
def send(sock, adresa_receptor, seq_nr, window, octeti_payload):
    '''
    Functie care trimite octeti ca payload catre receptor
    cu seq_nr dat ca parametru.
    Returneaza ack_nr si window curent primit de la server.
    '''
    # TO DO...
    flags = 'P'
    checksum = 0
    octeti_header_fara_checksum = create_header_emitator(seq_nr, flags, checksum)
    mesaj = octeti_header_fara_checksum + octeti_payload #octeti_payload = segment
    checksum = calculeaza_checksum(mesaj)
    octeti_header_cu_checksum = create_header_emitator(seq_nr, flags, checksum)
    mesaj = octeti_header_cu_checksum + octeti_payload

    sock.sendto(mesaj, adresa_receptor)

    return ack_nr, window


def main():
    parser = ArgumentParser(usage=__file__ + ' '
                                             '-a/--adresa IP '
                                             '-p/--port PORT'
                                             '-f/--fisier FILE_PATH',
                            description='Reliable UDP Emitter')

    parser.add_argument('-a', '--adresa',
                        dest='adresa',
                        default='receptor',
                        help='Adresa IP a receptorului (IP-ul containerului, localhost sau altceva)')

    parser.add_argument('-p', '--port',
                        dest='port',
                        default='10000',
                        help='Portul pe care asculta receptorul pentru mesaje')

    parser.add_argument('-f', '--fisier',
                        dest='fisier',
                        help='Calea catre fisierul care urmeaza a fi trimis')

    # Parse arguments
    args = vars(parser.parse_args())

    ip_receptor = args['adresa']
    port_receptor = args['port']
    fisier = args['fisier']

    adresa_receptor = (ip_receptor, port_receptor)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
    # setam timeout pe socket in cazul in care recvfrom nu primeste nimic in 3 secunde
    sock.settimeout(10)
    try:
        ack_nr, window = connect(sock, adresa_receptor)
        file_descriptor = open(fisier, 'rb')
        
        # TODO: send trebuie sa trimită o fereastră de window segmente
        # până primșete confirmarea primirii tuturor segmentelor
        # --- > while ack_nr != seq_nr + len(segment):
        segment = citeste_segment(file_descriptor)
        while ack_nr != seq_nr + window * len(segment):
            ack_nr, window = send(sock, adresa_receptor, seq_nr, window, segment)
            if ack_nr == seq_nr + len(segment):
                segment = citeste_segment(file_descriptor)
                seq_nr = ack_nr
        
        finalize(sock, adresa_receptor)
    except Exception as e:
        logging.exception(traceback.format_exc())
        sock.close()
        file_descriptor.close()
    finally:
        sock.close()


if __name__ == '__main__':
    main()
