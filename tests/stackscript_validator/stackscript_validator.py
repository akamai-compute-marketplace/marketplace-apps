#!/usr/bin/env python3

import requests, sys, hashlib, argparse
from rich.console import Console
from rich.table import Table

github_data = []
admin_data = []


def github_stackscript(username='akamai-compute-marketplace', branch='main', repo='marketplace-apps'):
    """
    Scrapes deploy scripts from Github repo to build the github_data list.
    Looks for '# STACKSCRIPT_ID:' in deploy script.
    """

    repo = f"{username}/{repo}"
    url = f"https://api.github.com/repos/{repo}/contents/deployment_scripts?ref={branch}"
    response = requests.get(url)

    if response.status_code == 200:
        apps = [item["name"] for item in response.json() if item["name"].startswith("linode-marketplace-")]

        for app in apps:
            appname = app.split("linode-marketplace-", 1)[-1]
            ssurl = f"https://raw.githubusercontent.com/{repo}/refs/heads/{branch}/deployment_scripts/linode-marketplace-{appname}/{appname}-deploy.sh"
            ssresp = requests.get(ssurl)
            stackscript = ssresp.text
            stackscript_id = None
            for line in stackscript.splitlines():
                if "# STACKSCRIPT_ID:" in line:
                    stackscript_id = line.split(":")[1].strip()
                    break
            hash_result = hashlib.md5(stackscript.encode()).hexdigest()
            github_data.append({"appname": f"{app}", "ssid": f"{stackscript_id}", "md5": f"{hash_result}"})
    else:
        print(f"FAILED: {response.text}")
        sys.exit(1)


def admin_stackscripts():
    """
    Grabs the stackscript ID from Github deploy scripts and makes request
    to linode API to get MD5 digest.
    """

    for stackscript_id in github_data:
        ssid = (stackscript_id['ssid'])
        stackscript_url = f"https://cloud.linode.com/api/v4/linode/stackscripts/{ssid}"
        response = requests.get(stackscript_url)

        if response.status_code == 200:
            data = response.json()
            stackscript = data['script']
            label = data['label']
            hash_result = hashlib.md5(stackscript.encode()).hexdigest()

            admin_data.append({"appname": f"{label}", "md5": f"{hash_result}"})
        else:
            admin_data.append({"appname": "", "md5": "", "error_status": f"{response.text}"})


def generate_report(report_type, output_format='table'):
    """
    Create table report for apps and checksums
    """

    # init table
    console = Console()
    table = Table(title="Deployment Script Checksum", show_lines=True)

    # column headers
    table.add_column("GitHub", justify="center", style="cyan")
    table.add_column("Stackscript", justify="center", style="magenta")
    table.add_column("MD5", style="green")
    table.add_column("Stackscript ID", style="yellow")
    table.add_column("Status", justify="center")

    if output_format == "table":
        if report_type == '--show-all':
            for i, github_app in enumerate(github_data):
                if admin_data[i]['appname'] != "" and admin_data[i]['md5'] != "":
                    if github_app['md5'] == admin_data[i]['md5']:
                        table.add_row(f"{github_app['appname']}", f"{admin_data[i]['appname']}",
                                      f"[cyan]{github_app['appname']}[/cyan]:\n{github_app['md5']}\n\n[magenta]{admin_data[i]['appname']}[/magenta]:\n{admin_data[i]['md5']}",
                                      f"{github_app['ssid']}", "[black on green]MATCH[/black on green]")
                    else:
                        table.add_row(f"{github_app['appname']}", f"{admin_data[i]['appname']}",
                                      f"[cyan]{github_app['appname']}[/cyan]:\n{github_app['md5']}\n\n[magenta]{admin_data[i]['appname']}[/magenta]:\n{admin_data[i]['md5']}",
                                      f"{github_app['ssid']}", "[black on yellow]MISMATCH[/black on yellow]")
                else:
                    table.add_row(f"{github_app['appname']}", "[black on red]ERROR[/black on red]",
                                  f"[cyan]{github_app['appname']}[/cyan]:\n{github_app['md5']}",
                                  f"{github_app['ssid']}",
                                  f"[black on red]{admin_data[i]['error_status']}[/black on red]")

        if report_type in ('--show-error', '--show-failed'):
            for i, github_app in enumerate(github_data):
                if admin_data[i]['appname'] == "" and admin_data[i]['md5'] == "":
                    table.add_row(f"{github_app['appname']}", "[black on red]ERROR[/black on red]",
                                  f"[cyan]{github_app['appname']}[/cyan]:\n{github_app['md5']}",
                                  f"{github_app['ssid']}",
                                  f"[black on red]{admin_data[i]['error_status']}[/black on red]")

        if report_type in ('--show-mismatch', '--show-failed'):
            for i, github_app in enumerate(github_data):
                if admin_data[i]['appname'] != "" and admin_data[i]['md5'] != "":
                    if github_app['md5'] != admin_data[i]['md5']:
                        table.add_row(f"{github_app['appname']}", f"{admin_data[i]['appname']}",
                                      f"[cyan]{github_app['appname']}[/cyan]:\n{github_app['md5']}\n\n[magenta]{admin_data[i]['appname']}[/magenta]:\n   {admin_data[i]['md5']}",
                                      f"{github_app['ssid']}", "[black on yellow]MISMATCH[/black on yellow]")

        if report_type == '--show-match':
            for i, github_app in enumerate(github_data):
                if admin_data[i]['appname'] != "" and admin_data[i]['md5'] != "":
                    if github_app['md5'] == admin_data[i]['md5']:
                        table.add_row(f"{github_app['appname']}", f"{admin_data[i]['appname']}",
                                      f"[cyan]{github_app['appname']}[/cyan]:\n{github_app['md5']}\n\n[magenta]{admin_data[i]['appname']}[/magenta]:\n   {admin_data[i]['md5']}",
                                      f"{github_app['ssid']}", "[black on green]MATCH[/black on green]")

        # only print table if not empty
        if table.rows:
            console.print(table)
        else:
            print(f"No data for {report_type}")

    elif output_format == "text":
        if report_type == '--show-all':
            for i, github_app in enumerate(github_data):
                if admin_data[i]['appname'] != "" and admin_data[i]['md5'] != "":
                    if github_app['md5'] == admin_data[i]['md5']:
                        print(f"[MATCH] {github_app['appname']}, {github_app['md5']}, {github_app['ssid']}")
                    else:
                        print(f"[MISMATCH] {github_app['appname']}, {github_app['md5']}, {github_app['ssid']}")
                else:
                    print(
                        f"[ERROR] {github_app['appname']}, {github_app['md5']}, {github_app['ssid']}: {admin_data[i]['error_status']}")

        if report_type in ('--show-error', '--show-failed'):
            for i, github_app in enumerate(github_data):
                if admin_data[i]['appname'] == "" and admin_data[i]['md5'] == "":
                    print(
                        f"[ERROR] {github_app['appname']}, {github_app['md5']}, {github_app['ssid']}: {admin_data[i]['error_status']}")

        if report_type in ('--show-mismatch', '--show-failed'):
            for i, github_app in enumerate(github_data):
                if admin_data[i]['appname'] != "" and admin_data[i]['md5'] != "":
                    if github_app['md5'] != admin_data[i]['md5']:
                        print(f"[MISMATCH] {github_app['appname']}, {github_app['md5']}, {github_app['ssid']}")

        if report_type == '--show-match':
            for i, github_app in enumerate(github_data):
                if admin_data[i]['appname'] != "" and admin_data[i]['md5'] != "":
                    if github_app['md5'] == admin_data[i]['md5']:
                        print(f"[MATCH] {github_app['appname']}, {github_app['md5']}, {github_app['ssid']}")


def main():
    parser = argparse.ArgumentParser(
        prog='Stackscript Checkum Validator',
        description='Peformed MD5 checks on Github and backend deploy scripts.')

    ################
    # report types #
    ################

    report = parser.add_mutually_exclusive_group(required=True)
    report.add_argument('--show-all', action='store_true', required=False, help='Show all apps status')
    report.add_argument('--show-error', action='store_true', required=False,
                        help='Show apps that have errors when fetching deployment script.')
    report.add_argument('--show-mismatch', action='store_true', required=False,
                        help='Show apps with failed MD5 checks.')
    report.add_argument('--show-failed', action='store_true', required=False,
                        help='Show apps with errors or failed MD5 checks.')
    report.add_argument('--show-match', action='store_true', required=False, help='Show apps that passed MD5 checks.')

    #################
    # report format #
    #################
    report_format = parser.add_argument_group("Report Format")
    report_format.add_argument('--table', action='store_true', required=False, help='Output in table format')
    report_format.add_argument('--text', action='store_true', required=False, help='Output in text format')

    ###############
    # github args #
    ###############

    gh = parser.add_argument_group("GitHub")
    gh.add_argument('-u', '--username', type=str, required=False, help='Github user name')
    gh.add_argument('-b', '--branch', type=str, required=False, help='Github branch')
    gh.add_argument('-r', '--repo', type=str, required=False, help='Github repository')

    ####################
    # arg conditionals #
    ####################

    args = parser.parse_args()

    if args.username and not args.branch:
        parser.error("Please provide branch")
    if args.branch and not args.username:
        parser.error("Please provide username")

    ############
    # cli args #
    ############

    if args.show_all:
        # run with defaults
        if not args.username and not args.branch:
            github_stackscript()
        else:
            github_stackscript(username=args.username, branch=args.branch, repo=args.repo)
        admin_stackscripts()
        if args.table:
            generate_report(report_type='--show-all', output_format='table')
        elif args.text:
            generate_report(report_type='--show-all', output_format='text')
        # run report with defaults
        else:
            generate_report(report_type='--show-all')

    if args.show_error:
        if not args.username and not args.branch:
            github_stackscript()
        else:
            github_stackscript(username=args.username, branch=args.branch, repo=args.repo)
        admin_stackscripts()
        if args.table:
            generate_report(report_type='--show-error', output_format='table')
        elif args.text:
            generate_report(report_type='--show-error', output_format='text')
        # run with defaults
        else:
            generate_report(report_type='--show-error')

    if args.show_failed:
        if not args.username and not args.branch:
            github_stackscript()
        else:
            github_stackscript(username=args.username, branch=args.branch, repo=args.repo)
        admin_stackscripts()
        if args.table:
            generate_report(report_type='--show-failed', output_format='table')
        elif args.text:
            generate_report(report_type='--show-failed', output_format='text')
        else:
            generate_report(report_type='--show-failed')

    if args.show_mismatch:
        if not args.username and not args.branch:
            github_stackscript()
        else:
            github_stackscript(username=args.username, branch=args.branch, repo=args.repo)
        admin_stackscripts()
        if args.table:
            generate_report(report_type='--show-mismatch', output_format='table')
        elif args.text:
            generate_report(report_type='--show-mismatch', output_format='text')
        # run with defaults
        else:
            generate_report(report_type='--show-mismatch')

    if args.show_match:
        if not args.username and not args.branch:
            github_stackscript()
        else:
            github_stackscript(username=args.username, branch=args.branch, repo=args.repo)
        admin_stackscripts()
        if args.table:
            generate_report(report_type='--show-match', output_format='table')
        elif args.text:
            generate_report(report_type='--show-match', output_format='text')
        # run with defaults
        else:
            generate_report(report_type='--show-match')


if __name__ == '__main__':
    main()