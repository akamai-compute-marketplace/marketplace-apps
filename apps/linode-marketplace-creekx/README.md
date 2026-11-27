# Linode creekX Deployment One-Click APP

creekX is a self-hosted live video server. One install takes streams in by RTMP (OBS), SRT,
RTSP, WebRTC (from a browser) and IP cameras by ONVIF, and plays them out by WebRTC (under a
second), low-latency HLS and HLS, records every live into a video library, sends lives on to
other platforms, and runs 24/7 channels from the library.

The app installs the release creekx.io serves at deployment time, the same way as
`curl -fsSL https://creekx.io/get.sh | sudo bash`, checked against its published checksum.

## Editions

| Edition     | Price                       | Notes                                      |
| :---------- | :-------------------------- | :----------------------------------------- |
| creekX Lite | Free forever                | creekx.io/get-lite.sh                     |
| creekX Pro  | USD 99 per server per month | Every deployment starts a 14-day Pro trial |

Bring your own licence: Akamai bills the Linode, creekX is licensed at
[creekx.io](https://creekx.io).

## Software Included

| Software   | Version | Description                                     |
| :--------- | :------ | :---------------------------------------------- |
| creekX     | Latest  | The application: API, app and admin command     |
| PostgreSQL | 16      | Database                                        |
| Caddy      | 2.6     | Web server and https certificates               |
| MediaMTX   | 1.21.1  | The live server (bundled by creekX's installer) |
| FFmpeg     | 8.1     | Conversion and recording                        |
| coturn     | 4.6     | WebRTC relay for viewers behind strict NAT      |
| Node.js    | 24.19   | creekX's runtime                                |

**Supported Distributions:**

- Ubuntu 24.04 LTS

## Linode Helpers Included

| Name     | Action                                                        |
| :------- | :------------------------------------------------------------ |
| Hostname | Sets the hostname                                             |
| Users    | Creates the limited sudo user                                 |
| SSH Key  | Writes the account's SSH key to the sudo user                 |
| SSH      | Optionally disables root login over SSH                       |
| UFW      | Firewall: SSH and web; creekX's installer opens its own ports |
| Fail2ban | Bans repeated failed SSH logins                               |

## Use our API

Deploy with the Linode API: `POST /linode/instances` with `"image": "linode/ubuntu24.04"`,
this app's StackScript id, and `stackscript_data`:

```json
{
  "soa_email_address": "you@example.com",
  "user_name": "admin",
  "disable_root": "No"
}
```

## Resources

- [creekX website](https://creekx.io)
- [creekX documentation](https://creekx.io/docs/)
- [creekX on GitHub](https://github.com/creekx-io/creekx-live-streaming-server)
- [Support: hello@creekx.io](mailto:hello@creekx.io)
- [Create a Linode Account](https://www.linode.com/docs/guides/creating-a-compute-instance/)
