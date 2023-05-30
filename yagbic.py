from github import Github
import argparse
import os

g = Github(os.environ.get('GITHUB_TOKEN'))

def main():

    args = setup_cli()

    repos_list = get_repos_list(args.org_user, args.include, args.exclude)
    template_content = get_template_content(args.template, args.replace)
    create_issues(args.org_user, repos_list, args.title, template_content, args.labels)

def setup_cli():

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='''
This is a CLI for creating issues on GitHub in batch. Authorization token needs to be passed as environment variable GITHUB_TOKEN.
You provide the user or org name and path to file with issue contents. This CLI will create issue by default in all repositories.

You have different options that you can use to customize CLI actions.

Example usage:
    GITHUB_TOKEN=MY_TOKEN python yagbic.py OWNER PATH_TO_MARKDOWN TITLE
    GITHUB_TOKEN=MY_TOKEN python yagbic.py OWNER PATH_TO_MARKDOWN TITLE -i repo_1,repo_2 -l "good first issue,area/ci-cd"
    GITHUB_TOKEN=MY_TOKEN python yagbic.py OWNER PATH_TO_MARKDOWN TITLE -e repo_1,repo_2,repo_3
    GITHUB_TOKEN=MY_TOKEN python yagbic.py OWNER PATH_TO_MARKDOWN TITLE -e repo_1,repo_2,repo_3 -r "PLACEHOLDER_1:CUSTOM_VALUE,PLACEHOLDER_2:CUSTOM VALUE"
'''
    )

    parser.add_argument('org_user', help='Name of user or organization where repositories are located.')
    parser.add_argument('template', help='Provide a path to a template file that must be a markdown file. It will be used as a source for newly created issue.')
    parser.add_argument('title', help='Provide issue title.')
    parser.add_argument('-e', '--exclude', help='Provide a comma separated list of repositories that this CLI should omit.')
    parser.add_argument('-i', '--include', help='Provide a comma separated list of repositories that this CLI should take into account.')
    parser.add_argument('-r', '--replace', help='Provide a comma separated list of values that should be replaced in the template. Something like: -r "PLACEHOLDER_1:CUSTOM_VALUE,PLACEHOLDER_2:CUSTOM VALUE", where PLACEHOLDER_1 is in the template and will be replaced with CUSTOM_VALUE')
    parser.add_argument('-l', '--labels', help='Provide a comma separated list of labels to add to created issue.')

    return parser.parse_args()

def list_repos(org_user):
    repos_list = []
    for repo in g.get_user(org_user).get_repos():
        repos_list.append(repo.name)

    return repos_list

def get_template_content(path, replace):
    content = ''
    with open(path, 'r') as file:
        content = file.read()

    if replace:
       replace_strings_list = replace.split(',')
       for replace_string in replace_strings_list:
           replacement_split = replace_string.split(':')
           placeholder_name = replacement_split[0]
           placeholder_value = replacement_split[1]
           content = content.replace(placeholder_name, placeholder_value)

    return content

def get_repos_list(org_user, includes, excludes):
    repos_list = ''
    
    if (includes is None):
        repos_list = list_repos(org_user)
    else:
         repos_list = includes.replace(" ", "").split(',')

    if excludes:
        repos_to_exclude = excludes.replace(" ", "").split(',')
        repos_list = [repo for repo in repos_list if repo not in repos_to_exclude]

    return repos_list

def create_issues(owner, repos, title, content, labels):
    labelsList = []

    if labels:
       labelsList = labels.split(',')


    for repo_name in repos:
        repo = g.get_repo(f'{owner}/{repo_name}')
        issue = repo.create_issue(title=title, body=content, labels=labelsList)
        print(f'Issue URL for {repo_name}: {issue.html_url}')

main()