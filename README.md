# **YARD**
*Yet Another Register Designer*

[![Build Status](https://travis-ci.org/raczben/yard.svg?branch=dev)](https://travis-ci.org/raczben/yard)
[![codecov](https://codecov.io/gh/raczben/yard/branch/dev/graph/badge.svg)](https://codecov.io/gh/raczben/yard/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Yard is a register interface generator tool for processor controlled FPGA system. Yard generates all
needed sources and documentation for a register interface, like:
 - HDL sources
 - C headers
 - Documentation
 - TCL scripts
 
 
## **Install**

`pip install yard-fpga`

### **Running**
If `<python>/bin` is added to your `PATH` you can run YARD simply with `yard` command. If not, you
can run via `python3 -m yard`


## **Usage**
To start source code generation just run:

`yard <yardfile>`

where *yardfile* is the *Yet Another Register Descriptor* file which is a yaml file. See YARD syntax
for more information


## **YARD syntax**
Here is a simple introduction for syntax of yard files. For more information see examples or
documentation under the doc direcotry.

```yaml
%YAML 1.2
---
name: yard_example          # The name of your custom peripheral
interfaces:                 # Usually you have only one interface...
- name: axi                 # ... lets name it and ...
  type: AXI                 # ... define the protocol ...
  description:              # Write a brief description for your peripheral.
  - Control/Status register interface.  
  registers:                # This is the most essential part, where we define the registers.
  - name: data              # The name of the register
    access: RW              # access shows that what operations (read/write) are valid on this regiter.
```

Yardfile above is the bare-minimal version of yardfiles.

**Register properties:**
 - *name* I suggest to keep names as short as possible, because decorators (pre/post-fixes) makes it longer.
   And (the goal is that) all appearance of the register contains comments, to help understand it.
 - *access* can be *RW*, *RO* and *WO* (Note that WO means *implement write event*, rather than, *write-only*)
 - *brief* A short description of the regiser. (One sentence)
 - *detail* A detailed description of the register.
 - *address* defines the address where this register will be located. This is an optional field. If
    it doesn't exist (or its value is negative or ~), the address of the register will be resolved
    automaticly be the YARD program. The value of the address can be an integer, or
    `<integer>:<integer>:<integer>` for register arrays.
    
For more regiser fields see examples or documentation under the doc direcotry.


---
## **Dev**
First I must thank you if you plan to make any improovements in YARD. Here is a short guide to start
to understand whats under the hood.

### **Test**
TBD.

### **Delivery**

Yard repo uses [setuptools][2] and [pbr][3] for project administration, versioning and releasing.

**Before** creating a new distribution it is recommended to clean git repository first `git clean -dxf`
to be sure to pack those files that you want. Because *pbr* derives all version from the latest *tag*
of the git repository, to create a new version you need to commit and tag the repository.

To create a new distribution run the following command:

`setup.py sdist`

Now you have a packed source distribution of the project in the *./dist/* folder. You can test it
installing locally.

To upload new distribution to pypi:

`twine  upload ./dist/yard* -r testpypi`

To test installation of the new version's test-upload:

`pip install yard-fpga -i https://test.pypi.org/simple`

To upload new distribution to pypi:

`twine  upload ./dist/yard*`

To test installation of the new version's test-upload:

`pip install yard-fpga`

---
## **License**
Note, that YARD is under [GPL-3.0][1] license, which means that all generated files *can* be used in
commertial products. However any improovments or modifications of this YARD project must be
published / distributed.

[2]: https://pypi.org/project/setuptools/
[3]: https://pypi.org/project/pbr/
[1]: https://github.com/raczben/yard/blob/master/LICENSE



