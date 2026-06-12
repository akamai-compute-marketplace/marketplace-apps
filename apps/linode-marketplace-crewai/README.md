# Linode CrewAI Quick Deploy App

CrewAI is an open-source framework for building and orchestrating AI agents that work together as a team to accomplish complex tasks. Instead of relying on a single large language model prompt, CrewAI allows developers to create specialized agents with distinct roles, responsibilities, and goals. These agents can collaborate, delegate work, share information, and execute multi-step workflows autonomously.

## Software Included

| Software  | Version   | Description               |
| :---      | :----     | :---                      |
| CrewAI    | `latest`  | CrewAI binary client      |

**Supported Distributions:**

- Ubuntu 24.04 LTS

## Deployment Details

Once your application has finished deploying you will be able to create your CrewAI agents. Issue the following from the terminal.

1. Create new crew

```bash
crewai create crew research
```

2. Install crew

```bash
crewai install --prerelease=allow
```

3. Run crew

```bash
crewai run
```

## Resource

- [Introduction - Getting Started](https://docs.crewai.com/en/introduction)
- [Knowledge - External Knowledge Sources](https://docs.crewai.com/en/concepts/knowledge)
- [Custom Tooling - Giving Tool to Agents](https://docs.crewai.com/en/guides/tools/publish-custom-tools)
