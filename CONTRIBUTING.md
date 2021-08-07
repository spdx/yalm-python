# Contributing
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
