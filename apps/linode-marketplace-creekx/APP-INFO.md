# creekX: app information for the Akamai Marketplace

Goes into the pull request as `apps/linode-marketplace-creekx/APP-INFO.md`, as Akamai's
`docs/CONTRIBUTING.md` asks (read 2026-11-27 on the `develop` branch).

**App Name**
creekX

**App README**
`README.md` in this folder.

**App Description** (112 words)
creekX is a self-hosted live video server for teams that need to own their streaming. One
instance takes streams in by RTMP from OBS, SRT, RTSP, WebRTC from a browser and IP cameras by
ONVIF, and plays them out by WebRTC with under a second of delay, low-latency HLS and HLS.
Every live is recorded into a video library, can be sent on to YouTube, Twitch and other
platforms at the same time, and the library can run as 24/7 channels. Watch links can be
private and expire. Everything runs on your instance, with no per-minute or per-viewer fees.
Every deployment starts a 14-day creekX Pro trial; Pro is USD 99 per server per month.

**Version Number**
The release creekx.io serves at deployment (2026.11.27 on the day of writing; always the
newest, read from `https://creekx.io/download/VERSION`).

**Support URL**
https://creekx.io/support/ (email: hello@creekx.io)

**Operating System**
Ubuntu 24.04 LTS

**Documentation**
`DOCUMENTATION.md` in this folder.

**Editions**

- creekX Lite: free forever, real-time. Install it with `curl -fsSL https://creekx.io/get-lite.sh | sudo bash`.
- creekX Pro: USD 99 per server per month; every deployment starts a 14-day Pro trial.

Licensing is bring-your-own-licence: Akamai bills the Linode, creekX is licensed at
https://creekx.io.

**Links**

- Website: https://creekx.io
- GitHub: https://github.com/creekx-io/creekx-live-streaming-server
- Privacy policy: https://creekx.io/privacy
- Terms of use: https://creekx.io/terms

## App Assets

To zip and attach to the pull request (`assets.zip`), from `deploy/marketplace/akamai/assets/`:

| File                         | What                                               |
| ---------------------------- | -------------------------------------------------- |
| `creekx-logo-full-color.svg` | Logo (wordmark), full colour, for dark backgrounds |
| `creekx-logo-white.svg`      | Logo (wordmark), all white                         |
| `creekx-mark-full-color.svg` | Icon, full colour (Cloud Manager)                  |
| `creekx-mark-white.svg`      | Icon, all white                                    |
| `screenshot-*.png`           | Home, Streams and 24/7 channels (for the guide)    |

**Brand Color 1 (HEX Code):** `#252525`
**Brand Color 2 (HEX Code):** `#c7ff9f`
