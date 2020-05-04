# Soluție

## 1. Traceroute

Am implementat soluția iar aici este output-ul:

### Ruta către IP1(124.42.105.232):
```
192.168.43.1)
gateway
IP12(10.0.0.1) - IP rezervat pentru retea locala - StamAcasa rdsnet.ro (10.0.0.1)
10.13.219.190
IP rezervat pentru o retea locala
10.2.0.61
IP rezervat pentru o retea locala
10.2.0.13
IP rezervat pentru o retea locala
10.2.0.14
IP rezervat pentru o retea locala
Socket timeout  timed out
Traceback (most recent call last):
  File "traceroute.py", line 29, in traceroute
    data, addr = icmp_recv_socket.recvfrom(63535)
socket.timeout: timed out

IP rezervat pentru o retea locala
82.76.255.177
IP18:  Country: Romania Region: Bucharest City: Bucharest
10.220.128.98
IP rezervat pentru o retea locala
10.220.142.131
IP rezervat pentru o retea locala
62.115.165.184
IP111:  Country: Romania Region: Bucharest City: Bucharest
89.149.185.22
IP112:  Country: United States Region: Georgia City: Atlanta
219.158.43.189
IP113:  Country: China Region: Beijing City: Jinrongjie
219.158.11.181
IP114:  Country: China Region: Beijing City: Jinrongjie
219.158.41.93
IP115:  Country: China Region: Beijing City: Jinrongjie
219.158.16.65
IP116:  Country: China Region: Beijing City: Jinrongjie
219.158.115.121
IP117:  Country: China Region: Guangdong City: Guangzhou
219.158.16.65
IP118:  Country: China Region: Beijing City: Jinrongjie
61.49.214.14
IP119:  Country: China Region: Beijing City: Beijing
```

### Ruta către IP2
```
IP21 - Oraș, Regiune, Țară
IP22 - Oraș, Regiune, Țară
IP23 - Oraș, Regiune, Țară
...
IP2N - Oraș, Regiune, Țară
```

### Ruta către IP3
```
IP31 - Oraș, Regiune, Țară
IP32 - Oraș, Regiune, Țară
IP33 - Oraș, Regiune, Țară
...
IP3N - Oraș, Regiune, Țară
```


## 2. Reliable UDP

### Emițător - mesaje de logging
Rulăm `docker-compose logs emitator` și punem rezultatul aici:
```
....
....
....
....
....
```


### Receptor - mesaje de logging
Rulăm `docker-compose logs receptor` și punem rezultatul aici:
```
....
....
....
....
....
```
