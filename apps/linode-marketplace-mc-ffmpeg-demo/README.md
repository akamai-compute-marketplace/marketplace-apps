## App Information
MainConcept FFmpeg Plugins Demo

### App Name
MainConcept FFmpeg Plugins Demo

### App description
[MainConcept FFmpeg Plugins](https://www.mainconcept.com/ffmpeg) make improving visual quality and performance quick and simple with advanced features that are not available with open source, such as Hybrid GPU acceleration and xHE-AAC audio format. Perfectly suited for both VOD and live production workflows, our FFmpeg plugins give you the best of both worlds.

Please note: Since these apps deploy software for proprietary applications, a license is required. The MainConcept Marketplace apps automatically deploy a demo version designed for research, testing, and/or proof of concept. To upgrade your version, contact [MainConcept](https://www.mainconcept.com/akamai-linode).


### Version Number
2.3

### Support
* [Documentation](https://www.mainconcept.com/ffmpeg)

### Operating Systems
Debian 11

### Documentation
[Documentation](https://www.mainconcept.com/ffmpeg)

[Documentation for Hybrid HEVC Encoder Plugin](https://www.mainconcept.com/hubfs/PDFs/User%20Guides/MainConcept%20Hybrid%20HEVC%20Encoder%20Plug-In%20for%20FFmpeg%20User%20Guide.pdf)

[Documentation for HEVC Decoder Plugin](https://www.mainconcept.com/hubfs/PDFs/User%20Guides/MainConcept%20HEVC%20Decoder%20Plug-In%20for%20FFmpeg%20User%20Guide.pdf)

[Documentation for AVC Broadcast Encoder Plugin](https://www.mainconcept.com/hubfs/PDFs/User%20Guides/MainConcept%20AVC%20Broadcast%20Encoder%20Plug-In%20for%20FFmpeg%20User%20Guide.pdf)

[Documentation for AVC Decoder Plugin](https://www.mainconcept.com/hubfs/PDFs/User%20Guides/MainConcept%20AVC%20Decoder%20Plug-In%20for%20FFmpeg%20User%20Guide.pdf)

[Documentation for VVC Encoder Plugin](https://www.mainconcept.com/hubfs/PDFs/User%20Guides/MainConcept%20VVC%20Encoder%20Plug-In%20for%20FFmpeg%20User%20Guide.pdf)

[Documentationf or MPEG-H Encoder Plugin](https://www.mainconcept.com/hubfs/PDFs/User%20Guides/MainConcept%20MPEG-H%20Encoder%20Plug-In%20for%20FFmpeg%20User%20Guide.pdf)

[Documentation for xHE-AAC Encoder Plugin](https://www.mainconcept.com/hubfs/PDFs/User%20Guides/MainConcept%20xHE-AAC%20Encoder%20Plug-In%20for%20FFmpeg%20User%20Guide.pdf)

[Documetation for MPEG-2 TS Broadcast Delivery Plugin](https://www.mainconcept.com/hubfs/PDFs/User%20Guides/MainConcept%20MPEG-2%20TS%20Broadcast%20Delivery%20Plug-In%20for%20FFmpeg%20User%20Guide.pdf)

[Documentation for MPEG-2 Production Format Encoder Plugin](https://www.mainconcept.com/hubfs/PDFs/User%20Guides/MainConcept%20MPEG-2%20Encoder%20Plug-In%20for%20FFmpeg%20User%20Guide.pdf)

[Documentation for FFmpeg Plugin Tutorial: Command Line](https://www.mainconcept.com/hubfs/PDFs/User%20Guides/MainConcept%20FFmpeg%20Plugin%20Tutorial%20-%20CommandLine%20Struture.pdf)

Documentation on Linode: /opt/mainconcept/omx/share/doc/

### Example Command Lines

AVC/H.264 video encoding from YUV:

```
ffmpeg -r 25.000000 -pix_fmt yuv420p -s 1920x1080 -i "1920x1080p_25p_YV12.yuv" -vf scale=1280:720 -b:v 3500k -c:v omx_enc_avc -omx_core libomxil_core.so -omx_name OMX.MainConcept.enc_avc.video -omx_param "preset=main:perf_level=10:acc_type=sw:[AVC Settings]:bit_rate_mode=0:bit_rate=100000:time_scale=20000000:num_units_in_tick=1000000" "1920x1080p_25p_YV12_ffmpeg.mp4"
```

HEVC/H.265 video and xHE-AAC audio transcoding from encoded media file:

```
ffmpeg -i input.mp4 -c:v omx_enc_hevc -c:a omx_enc_xheaac -b:v 1000k -b:a 32000 -profile:a 28 -omx_name:v OMX.MainConcept.enc_hevc.video -omx_param:v "force_omx_param=1:preset=main:acc_type=sw" -omx_name:a OMX.MainConcept.enc_xheaac.audio -omx_core libomxil_core.so output.mp4
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