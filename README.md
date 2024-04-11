# fabaccess_klipper

Very very early implementation of Klipper control via FabAccess.
It uses an HTTP API that talks to the FabAccess server via CapnProto

## printer.cfg
```
[fabaccess_klipper]
ip: HTTP API IP and port
machine: _machineid_
```
