# SPDX YALM: Yet Another License Matcher
SPDX YALM is a license matching library based on [the SPDX License Matching Guideline](https://spdx.dev/license-list/matching-guidelines/).

SPDX is an open standard for communicating software bill of material information. SPDX reduces redundant work by providing common formats for organizations and communities to share important data, thereby streamlining and improving compliance, security, and dependability.

Project YALM is implemented as the matching guideline compliant library - this library provides a way to compare license documents and templates in a standardized way.

## Features
*    An Interface which compares text against a license template using the license matching guidelines.
*    An Interface which returns all matching SPDX listed license ID's for any license text.
*    An interface which compares 2 license texts and returns a boolean indicating if the 2 licenses match per the license matching guidelines.
*    When there is no match, a return value is provided to describe where and why the license does not match.

## Installation
Ensure you have installed Python 3.9 or higher.

You can install this library via [PyPI](https://pypi.org/project/yalm/).
```
pip install yalm
```

## Contributing
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


## License
Copyright (c) 2021, SPDX YALM Developers.
Files in this repository are licensed under
[Apache License Version 2.0](https://github.com/spdx/tools-python/blob/master/LICENSE).

This Project is
- initially developed by [@anshuldutt21](https://github.com/anshuldutt21/)
as a part of CommunityBridge Linux Foundation 2020.
- updated by [@m1kit](https://github.com/m1kit) and released
as a part of Google Summer of Code 2021.
- with thanks to mentors [@goneall](https://github.com/goneall)
