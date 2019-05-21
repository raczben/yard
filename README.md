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

### **Processing stages**
Following chapters will describe the main behaviour of yard.

 1. Reading descriptor (*.yard)
 2. Filling all fields
 3. Generating sources
 
    1. Generating rjobs
    2. Template rendering
    3. Beautifying


#### **Reading descriptor**
First yard reads the descriptor `*.yard` file, which contains all (custom) information to generate
all source code. This descriptor contains eg.: the name of the module, the registers, and bitfields.

This step reads the descriptor into the `Database` (defined in the `core.py`).

#### **Filling all fields**
The next stage is fill all defaults and derived values. There are a huge amount of parameters, which
aren't filled by the user. There are some obvious parameters, which would require redundant `*.yard`
file. (Eg.: The defauld type of the register in HDL is vector type ie.: std_logic_vector. This
parameter filled by automaticly in this step.)

Other parameters can be derived from other values. (Eg.: If we want to implement a RW register it
should be located in the pif not in the core.)

Also all register adress should be resolved at this time.

This step creates a full detailed `Database`. In debug mode `~<modulename>_DB.yaml` will exported
countaining this, full detailed database next to the user descriptor `*.yard` file.

#### **Generating sources**

This step runs for each generating source file. This step consists of multiple sub-parts:
 1. First yard generates a source dependent data structure, called *render-jobs* (aka. *rjobs*). This
    sub-step derive values from the full-detailed-Database and generates a custom database for the
    given sourcefile. (If the given source file generation is not a complicated, this step can be
    ignored.) ~minimal_CBaseGenerator_rjobs.yaml In debug mode `~<modulename>_<generatorClassname>_rjobs.yaml`
    will exported, countaining the data of renderjobs next to the user descriptor `*.yard` file.
 2. Then *template rendering* starts. This sub-step starts the mako's template renderer with the
    rjobs data. This outputs the generated sourcefile.
 3. Beautifier is an optional sub-step, because it doesn't add any functional stuff to code,
    it just indents/beautify the generated code. However it is a recommended step, because mako's template
    engine cannot handle both well indened template file (which is required by the debvelopers) and 
    the well indened rendered source files (which is required by the users) This sub-step handles this.

---
### **Test**
Run unittests with the following command:

`pytest --cov=yard`

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
commertial products for free, at your own risk. However any improovments or modifications of this
YARD project must be published / distributed.

[2]: https://pypi.org/project/setuptools/
[3]: https://pypi.org/project/pbr/
[1]: https://github.com/raczben/yard/blob/master/LICENSE



