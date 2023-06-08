# Servicio de sensores Fracttal

## Descripción
Este servicio se encarga de obtener los datos de los sensores y enviarlos a la plataforma de Fracttal
para posteriormente convertirlos a csv y tener la trazabilidad de los mismos.

## Instalación
- [1] Para instalar el servicio se debe ejecutar el siguiente comando:

```bash
.cli/ setup
```
- [2] Para iniciar el servicio se debe ejecutar el siguiente comando:

```bash
.cli/ setup run
```
- [3] Para realizar pruebas unitarias se debe ejecutar el siguiente comando:

```bash
.cli/ test
```
- [4] Para detener el servicio se debe ejecutar el siguiente comando:

```bash
.cli/ stop
```
- [5] Para desinstalar el servicio se debe ejecutar el siguiente comando:

```bash
.cli/ uninstall
```

## Instrucciones de uso
- [1] Para poder utilizar el servicio, se necesita tener en la raiz del proyecto un archivo llamado "sensor.csv" con los datos de los sensores, el cual debe tener la siguiente estructura:

timestamp | sensor_id | machine_status