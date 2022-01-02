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

## Example Code
```
import yaml

license_text = "The text of the license here."
yalm.detect_license(license_text)
```

## License
Copyright (c) 2021, SPDX YALM Developers.
Files in this repository are licensed under
[Apache License Version 2.0](https://github.com/spdx/tools-python/blob/master/LICENSE).

## Credits
This Project is
- initially developed by [@anshuldutt21](https://github.com/anshuldutt21/)
as a part of CommunityBridge Linux Foundation 2020.
- updated by [@m1kit](https://github.com/m1kit) and released
as a part of Google Summer of Code 2021.
- with thanks to mentors [@goneall](https://github.com/goneall)
