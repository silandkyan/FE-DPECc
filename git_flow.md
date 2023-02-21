# install github locally and setup
in order to access github remotely via git from the local machine, it was not anymore sufficient to use the github username and password (2-factor-auth. disabled!). instead, github had to be installed on the local machine and then a remote connection was established. 

1. create a github account.

2. install github cli on linux: https://github.com/cli/cli/blob/trunk/docs/install_linux.md

3. authenticate remote connection: https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git

4. configure git locally:

`git config --global user.email "your.mail@server.de"`

`git config --global user.name "your name"`


# download public/remote repository to your local machine ("clone")
download repo from github to pwd:

`git clone https-to-repo`

move pwd to new repo folder:

`cd folder-of-repo`

check status of local repo:

`git status`


# workflow for creating a new feature branch

You do this if you want to create new functionality, correct or improve the code, etc. Such changes must not be developed within the main branch. Instead, open a new feature branch and do the development there.
Go to correct folder, then update repo to newest state:

`git pull`

open a new feature branch (here called "branch-name") to work on:

`git branch branch-name`

change to the new branch and check if all is correct:

`git switch branch-name`

`git status`

after some changes were made, add them (-A = all) to the commit list and commit your changes:

`git add -A`

`git commit -m "short comment what changed"`


publish the modifications in the central remote repo (will be reviewed before merging):

`git push -u origin branch-name`

when the branch goal is reached, it can be merged with main branch in github.

(Avoid merging with main locally:

`git switch main`

`git merge branch-name`

Merged branch can now be deleted if not anymore needed:
`git branch -d branch-name`)

After the branch was merged with main in github, the branch can be deleted directly on github. After that, update your local copy of the repo.

# Handling pull requests

to test proposed changes locally:
[https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/checking-out-pull-requests-locally](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/checking-out-pull-requests-locally)

git ID of pull request from github webpage, then fetch pull request and create new branch:

`git fetch origin pull/ID/head:BRANCH_NAME`

switch to new branch:

`git switch BRANCH_NAME`

now do all necessary tests and modifications; when done, push the branch up to github:

`git push origin BRANCH_NAME`

create new pull request with the branch and merge with main


