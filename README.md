# SPDX-Python-LicenseMatching
Implement SPDX License Matching in Python. Project in CommunityBridge Linux Foundation 2020. 
The Software Package Data Exchange (SPDX) specification is a standard format for communicating the components, licenses and copyrights associated with a software package. This Project is mainly based on implementing License Matching Techniques in Python. 

## Check if 2 License Texts match
License Texts are matched based on the [SPDX License Matching Guidelines](https://spdx.dev/license-list/matching-guidelines/). In order to implement License Matching between 2 License Texts, do the following steps.

Clone the Repository and move to the spdx-python-licensematching folder.

Move the files in the normalize_license_text folder.

Execute the command 
```bash
Python normalize.py <File1> <File2>
```

## Tests

In order to run tests, go to the Test directory and execute the command
```python
Python test_compare2license_texts.py
```

