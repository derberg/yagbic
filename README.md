<div align="center">
  <img src="yagbic.webp" alt="Yet Another GitHub Batch Issue Creator" width="50%">
</div>

## Overview

This project provides a CLI that you can use to create an issue in GitHub with the same content, in multiple repos. It also enables you to do the same but repo by repo if you want based on a template that you can customize through dedicated placeholders.

I use it as [AsyncAPI](https://www.asyncapi.com/) for example like this:
```bash
#this will create the same issue with the same title in all repos in asyncapi org except two listed under "-e" flag 
GITHUB_TOKEN=******** python yagbic.py asyncapi issue_content.md "Need for urgent changes in GitHub Actions automation" -e shape-up-process,glee-hello-world
```

## Usage

1. Just clone this repo
1. Install dependency: `pip install PyGithub`
1. Get commands list: `python yagbic.py --help`

```bash
usage: yagbic.py [-h] [-e EXCLUDE] [-i INCLUDE] [-r REPLACE] org_user template title

This is a CLI for creating issues on GitHub in batch. Authorization token needs to be passed as environment variable GITHUB_TOKEN.
You provide the user or org name and path to file with issue contents. This CLI will create issue by default in all repositories.

You have different options that you can use to customize CLI actions.

Example usage:
    GITHUB_TOKEN=MY_TOKEN python yagbic.py OWNER PATH_TO_MARKDOWN TITLE
    GITHUB_TOKEN=MY_TOKEN python yagbic.py OWNER PATH_TO_MARKDOWN TITLE -i repo_1,repo_2
    GITHUB_TOKEN=MY_TOKEN python yagbic.py OWNER PATH_TO_MARKDOWN TITLE -e repo_1,repo_2,repo_3
    GITHUB_TOKEN=MY_TOKEN python yagbic.py OWNER PATH_TO_MARKDOWN TITLE -e repo_1,repo_2,repo_3 -r "PLACEHOLDER_1:CUSTOM_VALUE,PLACEHOLDER_2:CUSTOM VALUE"

positional arguments:
  org_user              Name of user or organization where repositories are located.
  template              Provide a path to a template file that must be a markdown file. It will be used as a source for newly created issue.
  title                 Provide issue title.

options:
  -h, --help            show this help message and exit
  -e EXCLUDE, --exclude EXCLUDE
                        Provide a comma separated list of repositories that this CLI should omit.
  -i INCLUDE, --include INCLUDE
                        Provide a comma separated list of repositories that this CLI should take into account.
  -r REPLACE, --replace REPLACE
                        Provide a comma separated list of values that should be replaced in the template. Something like: -r "PLACEHOLDER_1:CUSTOM_VALUE,PLACEHOLDER_2:CUSTOM VALUE", where PLACEHOLDER_1 is in the template and will be replaced with CUSTOM_VALUE
```