import struct
import socket
import random
import logging

MAX_UINT32 = 0xFFFFFFFF
MAX_BITI_CHECKSUM = 16
MAX_SEGMENT = 1400

def compara_endianness(numar):
    '''
    https://en.m.wikipedia.org/wiki/Endianness#Etymology
        numarul 16 se scrie in binar 10000 (2^4)
        pe 8 biti, adaugam 0 pe pozitiile mai mari: 00010000
        pe 16 biti, mai adauga un octet de 0 pe pozitiile mai mari: 00000000 00010000
        daca numaratoarea incepe de la dreapta la stanga:
            reprezentarea Big Endian (Network Order) este: 00000000 00010000
                - cel mai semnificativ bit are adresa cea mai mica
            reprezentarea Little Endian este: 00010000 00000000
                - cel mai semnificativ bit are adresa cea mai mare 
    '''
    print ("Numarul: ", numar)
    print ("Network Order (Big Endian): ", [bin(byte) for byte in struct.pack('!H', numar)])
    print ("Little Endian: ", [bin(byte) for byte in struct.pack('<H', numar)])


def create_header_emitator(seq_nr, checksum, flags='S'):
    '''
    folosind struct.pack impachetati numerele in octeti si returnati valorile
    flags pot fi 'S', 'P', sau 'F'
    '''
    octeti = struct.pack('!LHH',seq_nr, checksum, ord(flags))
    return octeti


def parse_header_emitator(octeti):
    '''
    folosind struct.unpack despachetati numerele 
    din headerul de la emitator in valori si returnati valorile
    '''
    seq_nr, checksum, spf = struct.unpack("!LHB", octeti)
    flags = ''
    if spf & 0b100:
        # inseamna ca am primit S
        flags = 'S'
    elif spf & 0b001:
        # inseamna ca am primit F
        flags = 'F'
    elif spf & 0b010:
        # inseamna ca am primit P
        flags = 'P'
    return (seq_nr, checksum, flags)


def create_header_receptor(ack_nr, checksum, window):
    '''
        folosind struct.pack impachetati numerele in octeti si returnati valorile
        flags pot fi 'S', 'P', sau 'F'
    '''
    octeti = struct.pack('!LHH', seq_nr, checksum, window)
    return octeti


def parse_header_receptor(octeti):
    '''
        folosind struct.unpack despachetati octetii in valori si returnati valorile
    '''
    ack_nr, checksum, window = struct.unpack("!LHH", octeti)
    return (ack_nr, checksum, window)


def citeste_segment(file_descriptor):
    '''
        generator, returneaza cate un segment de 1400 de octeti dintr-un fisier
    '''
    yield file_descriptor.read(MAX_SEGMENT)


def exemplu_citire(cale_catre_fisier):
    with open(cale_catre_fisier, 'rb') as file_in:
        for segment in citeste_segment(file_in):
            print(segment)


def calculeaza_checksum(octeti):
    sum_check = 0
    octeti = list(struct.unpack("!HHHHHHHH", octeti))
    nr_max = 65535


    if len(octeti) % 2:
        octeti.append(0)

    for i in (0, len(octeti), 2):
        if i + 1 < len(octeti):
            a = octeti[i]
            b = octeti[i + 1]
            sum_check += (a + b) % nr_max
    
    sum_check = nr_max - sum_check
    return sum_check


def verifica_checksum(octeti):
    if calculeaza_checksum(octeti) == 0:
        return True
    return False


if __name__ == '__main__':
    compara_endianness(16)