# Contributing

# Contributing
The project is open-source software, and bug reports, suggestions, and most especially patches are welcome.

## Issues
SPDX YALM Python has a [project page on GitHub](https://github.com/m1kit/yalm-python) where you can [create an issue](https://github.com/m1kit/yalm-python/issues) to report a bug, make a suggestion, or propose a substantial change or improvement that you might like to make.

If you would like to work on a fix for any issue, please assign the issue to yourself prior to creating a patch. For a larger patch, you are encouraged to create a draft PR and communicate with the members.

## Patches
The source code for SPDX YALM Python is hosted on [GitHub](https://github.com/m1kit/yalm-python). Please review [open pull requests](https://github.com/m1kit/yalm-python/pulls) before committing time to a substantial revision. Work along similar lines may already be in progress.

1. Install [poetry](https://python-poetry.org/docs/#installation).
2. `poetry install`
3. Make changes
4. Test [WIP]


We use the GitHub flow that is described here: https://guides.github.com/introduction/flow/

So, whenever we have to make some changes to the code, we should follow these steps:
1. Create a new branch:
    `git checkout -b fix-or-improve-something`
2. Make some changes and the first commit(s) to the branch: 
    `git commit --signoff -m 'What changes we did'`
3. Push the branch to GitHub:
    `git push origin fix-or-improve-something`
4. Make a pull request on GitHub.
5. Continue making more changes and commits on the branch, with `git commit --signoff` and `git push`.
6. When done, write a comment on the PR asking for a code review.
7. Some other developer will review your changes and accept your PR. The merge should be done with `rebase`, if possible, or with `squash`.
8. The temporary branch on GitHub should be deleted (there is a button for deleting it).
9. Delete the local branch as well:
    ```
    git checkout master
    git pull -p
    git branch -a
    git branch -d fix-or-improve-something
    ```

Besides this, another requirement is that every change should be made to fix or close an issue: https://guides.github.com/features/issues/
If there is no issue for the changes that you want to make, create first an issue about it that describes what needs to be done, assign it to yourself, and then start working for closing it.

## Licensing
However you choose to contribute, please sign-off in each of your commits that you license your contributions under the terms of [the Developer Certificate of Origin](https://developercertificate.org/). Git has utilities for signing off on commits: `git commit -s` signs a current commit, and `git rebase --signoff <revision-range>` retroactively signs a range of past commits.
