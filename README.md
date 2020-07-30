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
## Compare a License and a Template
License templates are implemented on the basis of the [SPDX License Matching Guidelines](https://spdx.dev/license-list/matching-guidelines/). In order to use the feature  of comparing a license text and a template-

```bash
cd compare_template_text/
```
```python
python compare_template_text.py <TextFile> <TemplateFile>
```

## Tests

In order to run tests, go to the Test directory and execute the commands-

For Comparing 2 License Texts:
```python
python test_compare2license_texts.py
```

For comparing a License Text and a Template:
```python 
python test_compare_template_text.py
```
