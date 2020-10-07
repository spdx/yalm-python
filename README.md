# SPDX Python Library for LicenseMatching
A Python Library to implement SPDX License Matching. This Project is a result of CommunityBridge Linux Foundation 2020 contribution by [@anshuldutt21](https://github.com/anshuldutt21/).

Python : Version>=3.7

Home: https://github.com/anshuldutt21/spdx_python_licensematching/

Issues: https://github.com/anshuldutt21/spdx_python_licensematching/issues

# License
[Apache-2.0](https://github.com/spdx/tools-python/blob/master/LICENSE)

# Features

*    An Interface which compares text against a license template using the license matching guidelines.
*    An Interface which returns all matching SPDX listed license ID's for any license text.
*    An interface which compares 2 license texts and returns a boolean indicating if the 2 licenses match per the license matching guidelines.
*    When there is no match, a return value is provided to describe where and why the license does not match.

# Installation

Clone the repository
```bash
git clone https://github.com/anshuldutt21/spdx_python_licensematching.git
```
Go to the directory
```bash
cd spdx_python_licensematching
```
As always you should work in a virtualenv or venv. Setup a python virtual environment by this command.
```bash
virtualenv venv -p python3.7
```
Activate it using
```bash
source venv/bin/activate
```
Install the dependencies
```bash
pip install -e .
```

# Examples

There are some examples for how to use the code in the examples folder in the directory. Go to the examples/ and run the following files to see the output.

```python
python compare_license_texts.py
```

This file will compare any 2 sample texts which can be passed into the module and return the output.

```python
python compare_license_template_text.py
```
This file parses the sample text and the template provided in the example and matches them producing the desired output.

```python
python compare_all_ids.py
```
This file parses the sample text and matches it against all the license ids and returns matched licenses.

# How To Use

## Compare 2 License Texts
License Texts are matched based on the [SPDX License Matching Guidelines](https://spdx.dev/license-list/matching-guidelines/). In order to implement License Matching between 2 License Texts, do the following steps.

To match  TextFile_A and TextFile_B execute the file normalize.py in the following way.

```python
python normalize_license_text/normalize.py <Path_to_TextFile_A> <Path_to_TextFile_B>
```
After this step you would get an output depicting whether the license Textfiles match or not along with the text describing the mismatch possibilities.

## Compare a License Text with a License Template
License templates are implemented on the basis of the [SPDX License Matching Guidelines](https://spdx.dev/license-list/matching-guidelines/). In order to use the feature  of comparing a license text and a template, do the following steps.

To match TextFile_A and TemplateFile_A execute the file compare_normalized_files.py in the following way.

```python
python compare_template_text.py/compare_template_text.py <Path_to_TextFile_A> <Path_to_TemplateFile_A>
```

After this step you would get an output depicting whether the license Textfiles match with the License Template or not along with the text describing the mismatch possibilities.

## Compare a license Text against all License templates.

The match_against_all_templates folder implements matching of the input license text against all the data templates in the SPDX license data. To match a License Text against all the License Templates, do the following steps:

To match TextFile_A against all templates execute the file match_all_ids.py.py in the following way.

```python
python match_all_ids.py <Path_to_TextFile_A>
```

# Tests

In order to run tests run 

```python
python setup.py test
```

# Development process

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

# Dependencies

* Difflib : https://docs.python.org/3/library/difflib.html used for generating differences.
* Re : https://docs.python.org/3/library/re.html for handling regexes.
