## App Information
MainConcept XDCAM Transcoder Demo

### App Name
MainConcept XDCAM Transcoder Demo

### App description
[MainConcept XDCAM Transcoder](https://www.mainconcept.com/transcoders) is an optimized Docker container for file-based transcoding of media files into professional Sony camera formats like XDCAM HD, XDCAM EX, XDCAM IMX and DVCAM (XDCAM DV).

Please note: Since these apps deploy software for proprietary applications, a license is required. The MainConcept Marketplace apps automatically deploy a demo version designed for research, testing, and/or proof of concept. To upgrade your version, contact [MainConcept](https://www.mainconcept.com/akamai-linode).

### Version Number
2.3

### Support
* [Documentation](https://www.mainconcept.com/transcoders)

### Operating Systems
Ubuntu 20.04 LTS, Ubuntu 22.04 LTS, Debian 11

### Documentation
[Documentation](https://www.mainconcept.com/transcoders)

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

### Brand color 1 - highlight
Color code - #2E8BC4

### Brand color 2 - dark
Color code - #12365A

### Brand color 3 - dark
Color code - #041125


### Logo
-Light and dark logo included in assets folder.

Dark:
![dark](assets/mainconcept.svg)

Light:
![light](assets/white/mainconcept.svg)