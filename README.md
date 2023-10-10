# Configuraciones

## Crear 2 servidores SSH [origen|destino]

### Servidor Remoto

Crear contenedor docker

```sh
docker run --name server_remoto -d -p 3000:22 gchavezvs2019/server-ssh-alpine
```

Rescatar la IP del servidor

```sh
hostname -I
```

Acceder al HOST

```sh
ssh -p 3000 test@<IP_HOST_REMOTO>
```

Crear directorios/archivos

```sh
mkdir casilla_a
mkdir casilla_b
cd casilla_a
mkdir entrada
mkdir salida
mkdir buzon
cd entrada
echo "kokokdoaskoask" >> archivo1.txt
echo "kokokdoaskoask" >> archivo1.txt.CTR
cd ..
cd buzon
echo "kokokdoaskoask" >> archivo1.txt.RES
echo "kokokdoaskoask" >> archivo1.txt.AVI
cd ..
cd ..
cd casilla_b
mkdir entrada
mkdir salida
mkdir buzon
```

### Servidor Local

Crear contenedor docker

```sh
docker run --name server_local -d -p 3001:22 gchavezvs2019/server-ssh-alpine
```

Rescatar la IP del servidor

```sh
hostname -I
```

Acceder al HOST

```sh
ssh -p 3001 test@<IP_HOST_LOCAL>
```

Crear directorios/archivos

```sh
mkdir casilla_a
mkdir casilla_b
cd casilla_b
mkdir entrada
mkdir salida
mkdir buzon
cd entrada
echo "kokokdoaskoask" >> archivo2.txt
echo "kokokdoaskoask" >> archivo2.txt.CTR
cd ..
cd buzon
echo "kokokdoaskoask" >> archivo2.txt.RES
echo "kokokdoaskoask" >> archivo2.txt.AVI
cd ..
cd ..
cd casilla_a
mkdir entrada
mkdir salida
mkdir buzon
```

## Configurar en DB Mongo [Origen|Pivote|Destino]

Recordar levantar la imagen
