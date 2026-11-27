# Deploy creekX through the Akamai Marketplace

creekX is a self-hosted live video server: streams in by RTMP, SRT, RTSP, WebRTC and IP
cameras, out by WebRTC, low-latency HLS and HLS, recorded into a library, sent on to other
platforms, and 24/7 channels from the library. It runs on your own instance; nothing is
streamed through a third party.

## Deploying a Marketplace App

1. Open the Marketplace in Cloud Manager and choose **creekX**.
2. Fill in the fields below, choose a region and a plan, and select **Create Linode**.
3. Deployment takes about 10 minutes after the instance is running. It installs the release
   creekx.io serves at that moment (`https://creekx.io/get.sh`), checked against its
   published checksum.

### Required Distribution

- **Ubuntu 24.04 LTS**

### Suggested Plan

- **4 GB Shared CPU** for trying it and a few lives without conversion.
- **Dedicated CPU, 8 cores or more** for many lives, several qualities per live, or
  converting uploaded videos. Conversion and qualities are what use the processor.

### creekX Options

- **Your email** (required): you sign in to creekX with it, and Let's Encrypt is given it for
  the https certificate.

### Limited User and SSH (Marketplace required fields)

- **Limited sudo user** (required): created for you; its password is in its credentials file.
- **SSH public key** (optional): added to the limited user.
- **Disable root access over SSH** (optional).

### Domain (optional)

- **Linode API token, subdomain and domain**: to create a DNS record for your own domain.
  Without them creekX uses this instance's own name,
  `<ip-with-dashes>.ip.linodeusercontent.com`, with an https certificate, so going live from
  a browser works from the first minute.

## Getting Started after Deployment

### Credentials

Over SSH as the limited user:

```bash
cat ~/.credentials
```

It holds the sudo password, the creekX address, and the creekX owner email and password.

### Sign in

Open the creekX address from the credentials file (`https://...`). Sign in with the owner
email and password.

### Go live

- **From OBS:** Settings, Stream, Service "Custom": server `rtmp://<your address>/live`, and
  the stream key shown under **Streams** in creekX.
- **From a browser:** Streams, a stream, **Use my camera**.
- **Watch:** the stream's **Share** tab gives a watch link and an embed code.

### Ports opened in the firewall

22 (SSH), 80 and 443 (web), 1935/tcp (RTMP), 8554/tcp (RTSP), 8890/udp (SRT), 8189 tcp and
udp (WebRTC), 9100-9199/udp (MPEG-TS encoders), and 3478 plus 49160-49359/udp (WebRTC relay).

### Editions and licence

Every deployment starts a **14-day trial of creekX Pro**; no card is needed.

- **creekX Lite:** free forever and real-time. Install it on any Ubuntu 24.04 server with `curl -fsSL https://creekx.io/get-lite.sh | sudo bash`.
- **creekX Pro:** USD 99 per server per month.

Buy a licence at [creekx.io](https://creekx.io) and add it with `sudo creekx activate KEY`,
or in the app under More, Licence. Akamai bills the Linode; creekX is licensed separately.

### Look after it

- `sudo creekx status`, `sudo creekx logs -f`, `sudo creekx backup`.
- Upgrade to the newest release: `curl -fsSL https://creekx.io/get.sh | sudo bash`.
  Everything is kept; if the new version does not start, the previous one is put back.

## Resources

- Website: [creekx.io](https://creekx.io)
- Documentation: [creekx.io/docs](https://creekx.io/docs/)
- GitHub: [github.com/creekx-io/creekx-live-streaming-server](https://github.com/creekx-io/creekx-live-streaming-server)
- Support: hello@creekx.io
