# Linode Akamai MCP Gateway Client

The Akamai Model Context Protocol (MCP) Gateway is a managed service that helps you bridge AI agents and applications with the Akamai product ecosystem. This Quick Deploy Apps allows customers to connect LLMs as clients to Akamai's MCP Gateway and interact with various APIs from a single source.

## Software Included

| Software  | Version   | Description   |
| :---      | :----     | :---          |
| Claude Code | `latest`    | LLM client     |

**Supported Distributions:**

- Ubuntu 24.04 LTS

## Deployment Details

Akamai MCP Gateway URL:
- https://mcp.akamai.com/mcp


This application connects to Akamai's MCP Gateway. Users must provide their JWT Token as an UDF in Cloud Manager to connect to the Akamai MCP Gateway. If the connection to the MCP server is successful, Claude will display the following message:

```output
akamai:
  Scope: User config (available in all your projects)
  Status: ✓ Connected
  Type: http
  URL: https://mcp.akamai.com/mcp?token=**********
```

## Manaully Adding MCP via Claude

If for whatever reason the connection to the MCP is failed (bad JWT token), you will need to remove the MCP and it again. This is a straight forward thing to do.

1. Remove the akamai MCP entry.
```bash
claude mcp remove akamai
```

2. Add MCP gateway
```bash
export JTW_TOKEN=my_jwt_token
claude mcp add --transport http --scope user akamai "https://mcp.akamai.com/mcp?token=$JWT_TOKEN"
```

Be sure to update `my_jwt_token` with your own token value.

3. Confirm MCP connection.

Once you've added the MCP gateway to Claude, please verify that was able to connect.

```
claud mcp get akamai
```

## Authenticate to Anthropic

To start using Claude Code you will need to finish the setup and authenticate to your Anthropic account. Just call Claude from the command line and finish the setup.

```bash
claude
```

## Resources

- [Akamai MCP Gateway Documentation](https://techdocs.akamai.com/mcp-gateway/docs/welcome)
