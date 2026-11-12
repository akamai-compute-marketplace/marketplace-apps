---
title: "Deploy 5dive through the Linode Marketplace"
description: "Deploy 5dive, a team of AI agents you own and run from your phone, on a Linode Compute Instance."
published: 2026-11-12
keywords: ['5dive', 'ai agents', 'claude code', 'codex', 'marketplace']
tags: ["ubuntu", "marketplace", "linode platform", "cloud manager"]
external_resources:
- '[5dive on GitHub](https://github.com/5dive-ai/5dive)'
---

5dive turns a server into a team of AI agents that you own. Agents such as
Claude Code and Codex run around the clock as their own Linux users, share one
task list, and check each other's work. They run on the AI plan you already pay
for. Link the server to the free 5dive app to hire a ready-made team and talk to
it from your phone.

## Deploying a Marketplace App

{{% content "deploy-marketplace-apps-shortguide" %}}

{{% content "marketplace-verify-standard-shortguide" %}}

{{< note >}}
**Estimated deployment time:** 5dive should be fully installed within 5-10 minutes after the Compute Instance has finished provisioning.
{{< /note >}}

## Configuration Options

- **Supported distributions:** Ubuntu 24.04 LTS
- **Suggested plan:** a Shared CPU 4 GB plan. One small agent runs on 1 GB; each
  more agent needs roughly 0.5-1 GB.

### 5dive Options

{{% content "marketplace-required-limited-user-fields-shortguide" %}}

{{% content "marketplace-special-character-limitations-shortguide" %}}

## Getting Started after Deployment

1. Log in to the server over SSH as the sudo user you chose:
   `ssh <username>@<your-linode-ip>`. The sudo password is stored in
   `/home/<username>/.credentials`.
2. The login screen shows one line: open https://5dive.ai/self-host to link
   this server to your 5dive account and hire your team from your phone.

   ```
   Link this server to your 5dive account: https://5dive.ai/self-host
   ```

   The line goes away once the server is linked.
3. Prefer the command line? Run `sudo 5dive init` to set up your first agent.

## Credentials

| What | Where |
| :--- | :--- |
| Sudo user and password | `/home/<username>/.credentials` |
| AI keys you add later | saved on the server by 5dive, never shown in chat |

{{% content "marketplace-update-note-shortguide" %}}
