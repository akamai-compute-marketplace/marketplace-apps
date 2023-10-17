## App Information
MainConcept XDCAM Transcoder

### App Name
MainConcept XDCAM Transcoder

### App description
[MainConcept XDCAM Transcoder](https://www.mainconcept.com/mc2go) is an optimized Docker container for file-based transcoding of media files into professional Sony camera formats like XDCAM HD, XDCAM EX, XDCAM IMX and DVCAM (XDCAM DV).

### Version Number
2.3

### Support
* [Documentation](https://www.mainconcept.com/mc2go)

### Operating Systems
Ubuntu 20.04 LTS, Ubuntu 22.04 LTS, Debian 11

### Documentation
[Documentation](https://www.mainconcept.com/mc2go)

### Example MainConcept XDCAM Transcoder HTTP endpoints
The REST API does not require authentication. The functions use the following syntax:
http://[container-ip-addess]:[port]/rest/[api-version]/[function]/[parameters]
The "api-version" part in the URL only contains the major version, and with a leading "v". For 
MainConcept XDCAM Transcoder v2.0 the API version is "v1".

1. Get service name:
```GET http://[ip-addess]:[port]/rest/v1/service```

2. Get transcoding jobs:
```GET http://[ip-addess]:[port]/rest/v1/jobs```

3. Get details on a specific job:
```GET http://[ip-addess]:[port]/rest/v1/jobs/{JobID}```

4. Start transcoding job:
```POST http://[ip-addess]:[port]/rest/v1/jobs```

, with body

```
{
  "INPUT": "ftp://10.144.41.202:2121/test.mp4",
  "OUTPUT": "ftp://10.144.41.202:2121/test/xdcam_hd.mxf",
  "PRESETNAME": "XDCAM_HD_422_1920x1080_cbr_50mbit",
  "KEEP_CONTENT": "TRUE",
  "VERBOSITY": "DEFAULT"
}
```

### Brand color 1
Color code - #041125

### Brand color 2
Color code - #6DBA98

### Logo
Light and dark logo included in assets folder.

Light:
![light](assets/MC2GOXDCAM_White.svg)

Dark:
![dark](assets/MC2GOXDCAM.svg)
