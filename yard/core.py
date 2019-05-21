# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 12:46:42 2019

@author: usr
"""


# Import build in modules
#  - os needed for file and directory manipulation
#  - sys needed for Python path manipulations
#  - copy need to deep copy
import os
import sys
import copy
import shutil

# Import 3th party modules:
#  - yaml parse and write yaml (yard) files
#  - logging to write logs of running
#  - mako the templating engine. This will render the generated files.
import yaml
import logging
from mako.lookup import TemplateLookup
from mako.exceptions import RichTraceback

# import YARD modules
from . import util

# To run standalone we need to add this module to pythonpath.
yard_module_path = os.path.dirname(os.path.abspath(__file__))
yardpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(yardpath) 
resourcepath = os.path.join(yard_module_path, './resources')

# Setup logging 
logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(filename='yard.log', filemode='w', format='%(asctime)s - %(name)s: [%(levelname)s] %(message)s')

MIT_LICENSE = \
'''Copyright <YEAR> <COPYRIGHT HOLDER>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.'''


#MIT_LICENSE = fmt_comment(MIT_LICENSE)

def is_debug():
    return logging.getLogger().level == logging.DEBUG

'''

'''
def hdl_indent(hdl, indentUnit='  '):
    """ simple identation method for vhdl codes.
    """
    indentAfter = ('begin', 'if', 'else', 'process', 'for', 'case', 'when', 'entity', 'generic', 'port', 'architecture') 
    indentEnd = ('end', 'else', 'begin', 'when', ')')
   
    depth = 0
    ret = []
   
    for l in hdl.splitlines():
        l = l.lstrip()
        if l.startswith(indentEnd):
            depth -= 1
            if depth < 0:
                logging.error('depth < 0')
        ret.append(depth*indentUnit + l)
        if l.startswith(indentAfter):
            depth += 1
            if depth > 16:
                logging.error('depth > 16')
       
    return ret


def cBeautifierGoogle(src, indentUnit='  '):
    """ simple identation method for C codes.
    """
    from . import code_style_check
    lines = src.splitlines()
    code_style_check._CheckCodeStyle(lines)
       
    return [l.rstrip("\n\r") for l in lines]


def cBeautifierSimple(src, indentUnit='  '):
    """ simple identation method for C codes.
    """
    
    indentAfter = ('{') 
    indentEnd = ('}')
   
    depth = 0
    ret = []
   
    for l in src.splitlines():
        l = l.lstrip()
        if True in [x in l for x in indentEnd]:
            depth -= 1
            if depth < 0:
                logging.error('depth < 0')
        ret.append(depth*indentUnit + l)
        if True in [x in l for x in indentAfter]:
            depth += 1
            if depth > 16:
                logging.error('depth > 16')
       
    return ret


def tclBeautifierSimple(src, indentUnit='  '):
    """ simple identation method for C codes.
    """
    
    indentAfter = ('{') 
    indentEnd = ('}')
   
    depth = 0
    ret = []
   
    for l in src.splitlines():
        l = l.lstrip()
        
        depthIncr = sum([l.count(x) for x in indentAfter]) - sum([l.count(x) for x in indentEnd])
        
        if depthIncr<0:
            depth -= 1
            if depth < 0:
                logging.error('depth < 0')
        ret.append(depth*indentUnit + l)
        if depthIncr>0:
            depth += 1
            if depth > 16:
                logging.error('depth > 16')
       
    return ret
   
 
class YardException(Exception):
    pass

    
class Decorator():
    
    def __init__(self, caseMode=None, separator='_'):
        """The caseMode switch between separator or case of the return string:
            'l' or  'lower' returns_an_underscore_separeted_string    (separator = '_')
            'cC' or 'camelCase': returnsACammelCaseString    (separator = '')
            'CC' or 'CamelCase': ReturnsACammelCaseString    (separator = '')
            'u' or 'upper' or 'AllCaps': RETURNS_AN_ALL_CAPS_STRING    (separator = '_')
            None: reTuRns_A_StrING_AS_user_GiVe (separator = '_')
        The separator will be the separator string of the return string:
            '_' returns_an_underscore_separeted_string    (caseMode = 'lower')
        """
        self.caseMode=caseMode
        self.separator=separator
        
    
    @staticmethod
    def append(lst, toAppend):
        if toAppend is None:
            return
        if isinstance(toAppend, list):
            lst += [*toAppend]
            return 
        lst.append(str(toAppend))
        return 
    
    
    def decorate(self, name, prefix = None, postfix = None):
        """
        General decorator function.
        Returns a decorated string of the input parameters. It will concatenate the prefixes then
        the names then the postfixes. The first 3 parameter (name, prefix, postix)can be both string
        or list of strings.
        """
        
        nameList = []
        Decorator.append(nameList, prefix)
        Decorator.append(nameList, name)
        Decorator.append(nameList, postfix)
        
        if self.caseMode in ['l', 'lower']:
            nameList = [x.lower() for x in nameList]
        elif self.caseMode in ['CC', 'CamelCase']:
            nameList = [x.title() for x in nameList[1:]]
            nameList.insert(0, nameList[0].lower())
        elif self.caseMode in ['CC', 'CamelCase']:
            nameList = [x.title() for x in nameList]
        elif self.caseMode in ['u', 'upper', 'AllCaps']:
            nameList = [x.upper() for x in nameList]
            
        return self.separator.join(nameList)
    

class Controller():
    
    def __init__(self, datafile=None, db=None, renderJobs=None, renderJobsLoadFile=None):
        """
        """
        self.db = DataBase(datafile, db)
        
        if renderJobs is not None:
            self.renderJobs = renderJobs
        elif renderJobsLoadFile is not None:
            with open(renderJobsLoadFile) as f:
                self.renderJobs = yaml.safe_load(f)
                
                
    def doAll(self):
        logging.info("Starting fill all fields...")
        self.db.fillAllFields()
        
        logging.info("Starting resolveAddress...")
        self.db.resolveAddress()
        
        logging.info("Starting dumping...")
        
        if is_debug():
            self.db.export()
            
        for k, trg in self.db['targets'].items():
            logging.info("Starting rendering %s ", k)
            genClass = getattr(sys.modules[__name__],  trg['generatorClass'])
            gen = genClass(self.db)
            
            logging.info("  Starting generateRenderData...")
            gen.generateRenderData()
            
            if is_debug():
                gen.exportRenderJobs()
            
            logging.info("  Starting render...")
            gen.render()
    
    
class Generator():
    
    def __init__(self, db=None, datafile=None, renderJobs=None, renderJobsLoadFile=None):
        """
        """
        self.db = DataBase(datafile, db)
        
        if renderJobs is not None:
            self.renderJobs = renderJobs
        elif renderJobsLoadFile is not None:
            with open(renderJobsLoadFile) as f:
                self.renderJobs = yaml.safe_load(f)
        
        
    def do(self, db=None, datafile=None, renderJobs=None, renderJobsLoadFile=None):
        """ do all stuf from parsing to generating.
        All fields are optional, can be given in constructior
        
        Keyword arguments:
        db -- holds the parsed (raw) yard database
        datafile -- filepath for (raw) yard database
        renderJobs -- the Mako template file. Used by the render method
        """
        if datafile is not None or db is not None:
            self.db = DataBase(datafile, db)
            
        if renderJobs is not None:
            self.renderJobs = renderJobs
            
        logging.info("Starting fill all fields...")
        self.db.fillAllFields()
        
        logging.info("Starting resolveAddress...")
        self.db.resolveAddress()
        
        logging.info("Starting dumping...")
        self.db.export()
            
        logging.info("Starting generateRenderData...")
        self.generateRenderData()
        
        logging.info("Starting render...")
        self.render()
        
        
    def generateRenderData(self):
        """ returns the data for render the template.
        It is easier to write templates for preprocessed data, instead of
        dopping the raw or fuldetailed yard data to the template file. This
        method do this preprocessing. This is template dependent task so this
        method should be overridden for all template.
        
        Keyword arguments:
        """
        self.renderJobs[0]['renderdata'] = self.db
        
    def preRender(self):
        pass
        
    def postRender(self):
        pass
        
    def render(self, renderJobs=None):
        """ Does the render. 
        It goes threw the renderJobs and renders all.
        """
        if renderJobs is not None:
            self.renderJobs = renderJobs
            
        self.preRender()
        
        for k, job in self.renderJobs['jobs'].items():
            try:
                #
                # Render the file. Note, that the output of folowing codes is
                #  syntatically/semantically correct but hard to  read. So post process needed.
                #
                logging.info("  Start rendering jobs, named: '%s' ...", k)
                
                # fetch render template
                mylookup = TemplateLookup(directories=[resourcepath])
                mytemplate = mylookup.get_template(job['templateFile'])
                # DO the RENDER
                generated_code = mytemplate.render(
                        lic=MIT_LICENSE,
                        commondata = self.renderJobs['common'],
                        renderdata = job['renderdata']
                        )
                
                #
                # Beautifier
                # Make more readable the output file.
                #
                
                logging.info("  Start beautifier ...")
                # Fetch beautifier parameters:
                indentUnit=self.renderJobs['common']['indentUnit']
                beautifierFunc = job['beautifierFunc']
                method_to_call = getattr(sys.modules[__name__], beautifierFunc)
                # BEAUTIFY:
                generated_code = method_to_call(generated_code, indentUnit=indentUnit)
                
                # save file:
                outdir=os.path.join(self.db.get_yard_file_folder(), job['destinationPath'])
                os.makedirs(outdir, exist_ok=True)
                filename =  job['outFilename']
                outfile = os.path.abspath(os.path.join(outdir, filename))
                logging.info("  Saving file to %s ...", outfile)
                with open(outfile, 'w',  newline='\n') as f:
                    f.write('\n'.join(generated_code))
            except:
                traceback = RichTraceback()
                for (filename, lineno, function, line) in traceback.traceback:
                    print("File %s, line %s, in %s" % (filename, lineno, function))
                    print(line, "\n")
                print("%s: %s" % (str(traceback.error.__class__.__name__), traceback.error))
                raise
        
        self.postRender()
                
                
    def exportRenderJobs(self):
        genType = self.__class__.__name__
        filename = '~{}_{}_rjobs.yaml'.format(self.db['name'], genType)
        filename = os.path.join(self.db.get_yard_file_folder(), filename)
        logging.info("  Dumping reder jobs into %s ...", filename)
        yaml.Dumper.ignore_aliases = lambda *args : True
        with open(filename, 'w') as f:    
            f.write(yaml.dump(self.renderJobs))
    
    
class AxiGenerator(Generator):
    def __init__(self, db=None, datafile=None, renderJobs=None):
        """ Initialize the generator class.
        db or filename must given to Generator
    
        Keyword arguments:
        db -- holds the parsed (raw) yard dataBase
        datafile -- filepath for (raw) yard database
        makotmpl -- the Mako template file. Used by the render method
        """
        super().__init__(db, datafile, renderJobsLoadFile=os.path.join(resourcepath, 'cfg/axi_basic_defaults.yard'))


    @staticmethod
    def swapDir(port):
        """ Swaps the direction of a port
        """
        ret = copy.deepcopy(port)
        if port['dir'] == 'in':
            ret['dir'] = 'out'
        elif port['dir'] == 'out':
            ret['dir'] = 'in'
        else:
            raise Exception('swapDir(): Unknown direction!')
        AxiGenerator.decorate(ret)
        return ret
    
        
    @staticmethod
    def decorate(var):
        functionPostfixes = {'register': '', 'readEvent': '_r_e', 'writeEnable': '_w_e',}
        snPostFix = ''
        if var['parsedAddress']['serialNumber'] >= 0:
            snPostFix = '_{}'.format(var['parsedAddress']['serialNumber'])
        decoratedName = var['name'] + snPostFix + functionPostfixes[var['function']]
        if var['signalClass'] == 'port':
            dirPrefixes = {'in': 'i_', 'out': 'o_',}
            var['decoratedName'] = dirPrefixes[var['dir']] + decoratedName
            return var
        if var['signalClass'] == 'signal':
            functionPrefixes = {'reg': 'q_', 'wire': 'w_', 'combinational': 'c_'}
            var['decoratedName'] = functionPrefixes[var['driverType']] + decoratedName
            return var
        raise Exception('decorate(): Unknown signalType')
            
        
    def add(self, module, group, sig):
        self.decorate(sig)
        self.renderJobs['jobs'][module]['renderdata'][group].append(sig)
        return sig
    
    
    def addSignal(self, module, sig):
        sig['signalClass'] = 'signal'
        return self.add(module, 'signals', sig)
        
    
    def addRegSignal(self, module, sig):
        sig['driverType'] = 'reg'
        return self.addSignal(module, sig)

    
    def addWireSignal(self, module, sig):
        sig['driverType'] = 'wire'
        return self.addSignal(module, sig)

        
    def addCombinationalSignal(self, module, sig):
        sig['driverType'] = 'combinational'
        return self.addSignal(module, sig)

    
    def addPort(self, module, sig):
        sig['signalClass'] = 'port'
        return self.add(module, 'ports', sig)

         
    def addOutPort(self, module, sig):
        sig['dir'] = 'out'
        return self.addPort(module, sig)
    
    
    def addInPort(self, module, sig):
        sig['dir'] = 'in'
        return self.addPort(module, sig)

    
    def addWriteRegister(self, module, sig):
        self.add(module, 'writeRegisters', sig)
    
    
    def addReadRegister(self, module, sig):
        self.add(module, 'readRegisters', sig)
    
    
    def addAssignment(self, module, group, sigRd, sigDrv):
        self.renderJobs['jobs'][module]['renderdata'][group].append({
                'left': sigRd, # aka. reader
                'right': sigDrv # aka. driver
                })
    
    
    def connect(self, src, trg, srcPort, via='top'):
        """ Creates a signal connection between two  modules (from src to trg) via a 'top' module.
        This method adds an out port to src wired connection on toplevel and an input port to trg
        module.
        
        Keyword arguments:
        src -- (string) source; This will be the module key in renderJobs[module] structure
        trg -- (string) target; This will be the module key in renderJobs[module] structure
        srcPort -- (dict) virtual signal descriptor. This carries the name, datatype and other parameters.
        via -- (string, default=top) top level; This will be the module key in renderJobs[module] structure
        """
        wireDesc = copy.deepcopy(srcPort)
        
        self.addOutPort(src, srcPort)
        
        trgPort = self.swapDir(srcPort)
        
        self.addWireSignal(via, wireDesc)
        self.addAssignment(via, src + 'PortAssignments', srcPort, wireDesc)
        self.addAssignment(via, trg + 'PortAssignments', trgPort, wireDesc)
        self.addInPort(trg, trgPort)
        
        return trgPort
        
    
    def genSignalDescriptor(self, reg, **kwargs):
        """ Generates and returns a fictive, virtual signal definition. Then this virtual signal can
        be added to the render data.
        
        This method initialize all fields from the register properties, which can be overridden with
        kwargs. Finally it calculate the fully decorated datatype from the paramterers.
        """
        desc = {**reg}
        desc['defaultValue'] = None
        desc['resetValue'] = desc['reset']
        desc['addressInBytes'] = desc['parsedAddress']['value'][0]
        desc={**desc, **kwargs}
        if desc['width'] < 0:
            desc['fulltype'] = desc['type']
        else:
            desc['fulltype'] = desc['type'] + '(' + str(desc['width']-1) + ' downto 0)'
        return desc
    
    
    def genRegisterDescriptor(self, reg, **kwargs):
        """ Generates and returns a fictive, virtual data register (ie. the register which is
        accessible via the register interface.) definition. Then this virtual signal can be added to
        the render data.
        """
        return self.genSignalDescriptor(reg,
                                function = 'register',
                                   )
        
        
    def genReadEventDescriptor(self, reg, **kwargs):
        """ Generates and returns a fictive, virtual read event signal definition. Then this virtual
        signal can be added to the render data.
        """
        return self.genSignalDescriptor(reg,
                                   function = 'readEvent',
                                   type = 'std_logic',
                                   width = -1
                                   )
    
    
    def genWriteEnableDescriptor(self, reg, **kwargs):
        """ Generates and returns a fictive, virtual write enable event signal definition. Then this
        virtual signal can be added to the render data.
        """
        return self.genSignalDescriptor(reg,
                                   function = 'writeEnable',
                                   type = 'std_logic',
                                   width = -1
                                   )
    
    
    def generateRenderData(self):
        """ Returns the data for render the template. This is the core and most complicated part of
        the generation.
        
        It is easier to write templates for preprocessed data, instead of dopping the raw or
        fuldetailed yard data to the template file. This method do this preprocessing.
        """
                
        #
        # Generate common and default fields
        #
        
        logging.info("  Generating common and default fields...")
        self.renderJobs['common'] = {**self.renderJobs['common']}
        # self.renderJobs['common'] = {**self.renderJobs['common'], **self.db['configuration']['hdl']}
        
        # PIF
        pifdata = self.renderJobs['jobs']['pif']['renderdata']
        pifdata['entityName'] = self.db['name'] + '_pif'
        pifdata['dataWidth'] = self.db.getDatawidth(0)
        self.renderJobs['jobs']['pif']['renderdata'] = pifdata
        
        # CORE
        coredata = self.renderJobs['jobs']['core']['renderdata']
        coredata['entityName'] = self.db['name'] + '_core'
        coredata['dataWidth'] = self.db.getDatawidth(0)
        self.renderJobs['jobs']['core']['renderdata'] = coredata
        
        # TOP
        topdata = self.renderJobs['jobs']['top']['renderdata']
        topdata['entityName'] = self.db['name'] + '_top'
        topdata['coreEntityName'] = coredata['entityName']
        topdata['pifEntityName'] = pifdata['entityName'] = self.db['name'] + '_pif'
        topdata['dataWidth'] = self.db.getDatawidth(0)
        self.renderJobs['jobs']['top']['renderdata'] = topdata
        
        #
        # Generate data for registers.
        # We go threw each registers and generate all files (PIF, CORE, TOP) parallel
        #
        if self.db['targets']['hardware']['rollOutArrays']:
            self.db = copy.deepcopy(self.db)
            self.db.rollOutStride()
        
        logging.info("  Generating fields for all registers...")
        for reg in self.db['interfaces'][0]['registers']:
            
            #
            # First generate write enable and read event signals (if they are needed.)
            #
            if reg['hasWriteEnable']:
                pifWeDesc = self.genWriteEnableDescriptor(reg)
                coreWeDesc = self.connect('pif', 'core', pifWeDesc)
                self.add('pif', 'writeEnables', pifWeDesc)
            if reg['hasReadEvent']:
                pifReDesc = self.genReadEventDescriptor(reg)
#                coreReDesc = self.connect('pif', 'core', pifReDesc)
                self.add('pif', 'readEvents', pifReDesc)
                
            #
            # Generate data for the register itself
            #
            
            # define the register where it should be located:
            regDesc = self.genRegisterDescriptor(reg)
            self.addRegSignal(reg['location'], regDesc)
            
            # The structure is a bit different depending on the location of the register.
            if reg['location'] == 'pif':
                if reg['access'] in ['RW', 'WO']:
                    self.addWriteRegister('pif', regDesc)
                if reg['access'] in ['RW', 'RO']:
                    self.addReadRegister('pif', regDesc)
                
                # Connect from PIF to CORE
                pifPortDesc = self.genRegisterDescriptor(reg)
                self.addAssignment('pif', 'IOAssignments', pifPortDesc, regDesc)
                corePortDesc = self.connect('pif', 'core', pifPortDesc)
                
            elif reg['location'] == 'core':
                # Make it writable if it needed
                if reg['access'] in ['RW', 'WO']:
                    self.renderJobs['jobs']['core']['renderdata']['writeRegisters'].append({
                            'writeEn': coreWeDesc,
                            'register': regDesc
                            })
                
                # Make it readable if it is needed
                if reg['access'] in ['RW', 'RO']:
                    corePortDesc = self.genRegisterDescriptor(reg)
                    self.addAssignment('core', 'IOAssignments', corePortDesc, regDesc)
                    pifPortDesc = self.connect('core', 'pif', corePortDesc)
                    self.addReadRegister('pif', pifPortDesc)
                    
            else:
                logging.error('Undefined location in reg: %s : location: %s', reg['name'], reg['location'])

    
class CBaseGenerator(Generator):
    def __init__(self, data=None, datafile=None, renderJobs=None):
        """ Initialize the generator class.
        data or filename must given to Generator
    
        Keyword arguments:
        data -- holds the parsed (raw) yard data
        datafile -- filepath for (raw) yard data
        makotmpl -- the Mako template file. Used by the render method
        """
        super().__init__(data, datafile, renderJobsLoadFile=os.path.join(resourcepath, 'cfg/c_basic_defaults.yard'))
        self.fnDecorator = Decorator('lower', '_')
        self.defDecorator = Decorator('upper', '_')


    def decorateSetterFunctionName(self, reg):
        return self.fnDecorator.decorate(reg['name'], 'set')


    def decorateGetterFunctionName(self, reg):
        return self.fnDecorator.decorate(reg['name'], 'get')


    def generateRenderData(self):
        """ Returns the data for render the template. This is the core and most complicated part of
        the generation.
        
        It is easier to write templates for preprocessed data, instead of dopping the raw or
        fuldetailed yard data to the template file. This method do this preprocessing.
        """
        
        #
        # Generate header informations
        #
        
        # Source
        sourcedata = {**self.renderJobs['common']}
        # sourcedata = {**self.renderJobs['common'], **self.db['configuration']['software']}
        sourcedata['dataWidth'] = self.db.getDatawidth(0)
        self.renderJobs['common'] = sourcedata
        
        if self.db['targets']['software']['rollOutArrays']:
            self.db = copy.deepcopy(self.db)
            self.db.rollOutStride()
        #
        # Generate data for registers.
        # We go threw each registers and generate all files (PIF, CORE, TOP) parallel
        #
        
        self.renderJobs['common']['headerGuardDefine'] = self.defDecorator.decorate(self.db['name'], '_', '_')
        
        for iface in self.db['interfaces']:
            for reg in iface['registers']:
                regData = {
                        'setter': None,
                        'getter': None,
                        'bitFields': []
                        }
                #
                # Generate data for the register itself
                #
                sn = reg['parsedAddress']['serialNumber']
                if sn < 0:
                    sn = None
                regData['addressDefineName'] = self.defDecorator.decorate(reg['name'], 'REG_OFFS', sn)
                regData['addressDefineValue'] = reg['parsedAddress']['value'][0]
                
                regData['addressIncrement'] = reg['parsedAddress']['increment']
                
                if reg['access'] in ['RW', 'WO']:
                    # Generate setter data:
                    regData['setter'] = {}
                    regData['setter']['functionName'] = self.decorateSetterFunctionName(reg)
                if reg['access'] in ['RW', 'RO']:
                    regData['getter'] = {}
                    regData['getter']['functionName'] = self.decorateGetterFunctionName(reg)
                    
                self.renderJobs['common']['registers'].append(regData)

    def postRender(self):
        src = os.path.join(resourcepath, 'include', 'regutil.h')
        dst = os.path.join(self.db.get_yard_file_folder(), self.renderJobs['jobs']['headerBase']['destinationPath'], 'regutil.h')
        shutil.copyfile(src, dst)
   
class TCLBaseGenerator(Generator):

    def __init__(self, data=None, datafile=None, renderJobs=None):
        """ Initialize the generator class.
        data or filename must given to Generator
    
        Keyword arguments:
        data -- holds the parsed (raw) yard data
        datafile -- filepath for (raw) yard data
        makotmpl -- the Mako template file. Used by the render method
        """
        super().__init__(data, datafile, renderJobsLoadFile=os.path.join(resourcepath, 'cfg/tcl_basic_defaults.yard'))
        self.decorator = Decorator('lower', '_')


    def decorateSetter(self, reg):
        return self.decorator.decorate(reg['name'], 'set')


    def decorateGetter(self, reg):
        return self.decorator.decorate(reg['name'], 'get')


    def decorateBFSetter(self, reg, bf):
        return self.decorator.decorate(reg['name'], ['set', 'bf'], bf['name'])
    
    
    def decorateBFGetter(self, reg, bf):
        return self.decorator.decorate(reg['name'], ['get', 'bf'], bf['name'])


    def generateRenderData(self):
        """ Returns the data for render the template. This is the core and most complicated part of
        the generation.
        
        It is easier to write templates for preprocessed data, instead of dopping the raw or
        fuldetailed yard data to the template file. This method do this preprocessing.
        """
        
        #
        # Generate header informations
        #
        
        # Source
        # sourcedata = {**self.renderJobs['common'], **self.db['configuration']['software']}
        sourcedata = {**self.renderJobs['common']}
        sourcedata['dataWidth'] = self.db.getDatawidth(0)
        self.renderJobs['common'] = sourcedata
        
        self.renderJobs['jobs']['sourceBase']['outFilename'] = self.db['name']+'.tcl'
        
        
        if self.db['targets']['testTCL']['rollOutArrays']:
            self.db = copy.deepcopy(self.db)
            self.db.rollOutStride()
        #
        # Generate data for registers.
        # We go threw each registers and generate all files (PIF, CORE, TOP) parallel
        #
        
        for iface in self.db['interfaces']:
            for reg in iface['registers']:
                regData = {
                        'setter': None,
                        'getter': None,
                        'bitFields': []
                        }
                
                #
                # Generate data for the register itself
                #
                addressDefineName = 'REG_OFFS_' + reg['name'].upper() 
                regData['addressDefineName'] = addressDefineName
                addr = reg['parsedAddress']['value'][0]
                            
                addrDefData = {'addressDefineName': addressDefineName, 'address':  addr}
                
                if reg['access'] in ['RW', 'WO']:
                    # Generate setter data:
                    regData['setter'] = {}
                    regData['setter']['functionName'] = self.decorateSetter(reg)
                if reg['access'] in ['RW', 'RO']:
                    regData['getter'] = {}
                    regData['getter']['functionName'] = self.decorateGetter(reg)
                    
                self.renderJobs['common']['registers'].append(regData)
                self.renderJobs['common']['addressDefines'].append(addrDefData)
                
                if reg['fields']:
                    for bf in reg['fields']:
                        bfData = {
                            'setter': None,
                            'getter': None,
                            'bitFields': []
                            }
                        addressDefineName = 'BF_START_{}_{}'.format(reg['name'].upper(), bf['name'].upper() )
                        bfData['addressDefineName'] = addressDefineName
                        addr = reg['parsedAddress']['value'][0]
                        addrDefData = {'addressDefineName': addressDefineName, 'address':  addr}
                        bfData['start'] = bf['_positionStart']
                        bfData['length'] = bf['_positionLength']
            
                        if reg['access'] in ['RW', 'WO']:   # TODO reg -> bf
                            # Generate setter data:
                            bfData['setter'] = {}
                            bfData['setter']['functionName'] = self.decorateBFSetter(reg, bf)
                        if reg['access'] in ['RW', 'RO']:
                            bfData['getter'] = {}
                            bfData['getter']['functionName'] = self.decorateBFGetter(reg, bf)
                            
                        regData['bitFields'].append(bfData)

    
class DataBase():
    _defaults = None
    _defaults_loaded = False
    
    
    def __init__(self, yard_file=None, other=None):
        """ Initialize the generator class.
        other or filename must given to DataBase
    
        Keyword arguments:
        yard_file -- filepath for (raw) yard data
        other -- copies data from other
        """
        
        self.dataDirthy=True
        self.addressDirthy=True
        self.data={}
        self.yard_file=yard_file
        self.addressMap={}
        self._init_defaults()
        
        if other is not None:
            self.dataDirthy   = other.dataDirthy
            self.addressDirthy= other.addressDirthy
            self.data         = other.data
            self.addressMap   = other.addressMap
            self.yard_file    = other.yard_file
            return 
            
        if yard_file is not None:
            with open(yard_file) as f:
                self.data = yaml.safe_load(f)
            return
        
        # If no data or file given
        self.loadDefaults()
        
    def get_yard_file_folder(self):
        return os.path.dirname(os.path.abspath(self.yard_file))
        
    def __getitem__(self, key):
        return self.data[key]


    def __setitem__(self, key, value):
        self.data[key] = value
        
        
    @staticmethod
    def _init_defaults(defaultFile='cfg/yard_defaults.yard'):
        ''' Loads the default settigs of the DataBase. Later these settings will be filled empty
        paramteres, which was not defined by the user.
        '''
        if not DataBase._defaults_loaded:
            filename = os.path.join(resourcepath, 'cfg/yard_defaults.yard')
            with open(filename) as f:
                DataBase._defaults = yaml.safe_load(f)
            DataBase._defaults_loaded = True
        
        
    def loadDefaults(self, gently=True, defaultFile='cfg/yard_defaults.yard'):
        """ Fill all fields with default values which was not defined previously (in the .yard file)
        """
        self._init_defaults(defaultFile)
        
        defaults = copy.deepcopy(self._defaults)
        
        self.data = {**defaults['generalDefaults'], **self.data}
        
        for iface in self.data['interfaces']:
            self.dictMrg(iface, defaults['interfaceDefaults'])
            
            for reg in iface['registers']:
                self.dictMrg(reg, defaults['registerDefaults'])
                
                if reg['fields'] is not None:
                    for field in reg['fields']:
                        self.dictMrg(field, defaults['fieldsDefaults'])
       
        
    def getDatawidth(self, ifid=0):
        """ returns the datawidth of given interface. (This will be the default
        width of the registers)
        """
        try:
            ifacetype = self.data['interfaces'][ifid]['type']
        except IndexError:
            logging.error('No interface with ID: ' + str(ifid))
            raise YardException('No interface with ID: ' + str(ifid))
            
        if ifacetype.lower() in ['axi', 'axi32', 'axi-32']:
            return 32
        elif ifacetype.lower() in ['axi64', 'axi-64']:
            return 64
        else:
            logging.error('Unknown interface type')
            raise YardException('Unknown interface type')
        
        
    def _mapAddressRegister(self, reg, test=False):
        """ Map the address of a register.
        
        This method fetch the address (or more addresses if this is a stride register) of the given
        register. If there is no address conflict (already used address, unaligned address) it
        inserts to `addressMap` dict, which holds all address and registers.
        """
        success = True
        
        reg['parsedAddress']['value'] = self._getAddressValues(reg)
            
        address = reg['parsedAddress']['value']
        name = reg['name']
        if not isinstance(reg['parsedAddress']['value'], list):
            success = False
            if test:
                return success
            raise ValueError("reg['parsedAddress']['value'] must be list; name=" + name) 
        
        granulity = self.getDatawidth(0)/8
        
        if bool(set(address) & set(self.addressMap.keys())):
            success = False
            if test:
                return success
            logging.error('Address conflict: %h, %s, %s',  address, self.addressMap[address], name)
            self.addressDirthy=True
        elif True in [x % granulity != 0 for x in address]:
            success = False
            if test:
                return success
            logging.error('Unaligned address found: %h, %s', address, name)
        else:
            for addr in reg['parsedAddress']['value']:
                self.addressMap[addr] = reg
            return success
        
        
    def mapAddresses(self, data=None):
        """ Explores the addresses in the interface. It just maps not resolve
        'auto' setted ones. This method can find address conflits too.
        """
        if data is not None:
            self.data = data
        # let assume that all address are presetted, so set addressDirthy=False
        self.addressDirthy=False
        
        for iface in self.data['interfaces']:
            for reg in iface['registers']:
                address = reg['parsedAddress']['value']
                if address is None:
                    if self.addressDirthy==False:
                        logging.info("  Note, that one or more address are set to auto, so resolving needed.")
                    self.addressDirthy=True
                else:                    
                    self._mapAddressRegister(reg)
        return self.addressMap
        
        
    def resolveAddress(self):
        """ Resolve the address of all registers.
        
        `None` or `-1` address value (ind the yard file) means 'auto' the addresses. This method
        will resolve (give valid integers) for these register address.
        """
        
        # First map all explicitly set address, to prevent overlap auto-set address.
        self.mapAddresses()
        
        nextAddr = 0
        granulity = int(self.getDatawidth(0)/8)
        # let assume that all address are presetted, so set addressDirthy=False
        self.addressDirthy=False
        for iface in self.data['interfaces']:
            for reg in iface['registers']:
                if reg['parsedAddress']['value'] is None:
                    # do - while loop
                    i = 0
                    while True:
                        i+=1
                        if i>10000:
                            raise Exception('Too many iteration... ({})'.format(reg['name']))
                        reg['parsedAddress']['start'] = nextAddr
                        nextAddr += granulity
                        if self._mapAddressRegister(reg, test=True):
                            logging.debug('Register address resolved. {} -> {}'.format(reg['name'], reg['parsedAddress']['value']))
                            break
        return self.addressMap
    
    
    @staticmethod
    def dictMrg(highDict, lowDict):
        """ Merge two dict.
        
        The first parameter is the 'high priority' dict, the second is the 'low priority'. This
        method inserts items from the lowDict (second parameter) into the highDict (first parameter).
        This method keep the reference (pointer) of the highDict.
        """
        tmp = {**copy.deepcopy(lowDict), **highDict}
        highDict.update(tmp)

      
    @staticmethod
    def _getAddressValues(reg):
        """ Returns all address values of a register.
        Note that 'stride' feature will place one register into multiple address. This will results
        a true-list (with multiple element). If this register is a simple register (not stride) the
        return value will contain only one element (the address of this simple register).
        """
        startAddr = reg['parsedAddress']['start']
        count     = reg['parsedAddress']['count']
        increment = reg['parsedAddress']['increment']
        if isinstance(startAddr, int) and startAddr >= 0: 
            if count < 0:
                count = 1
            return [x for x in range(startAddr, startAddr+increment*count, increment)]
        return None
    
    
    def addInterface(self, iface=None):
        """ Adds a default interface to module.
        
        This is a used by HWH -> YARD converter.
        """
        if iface is None:
            iface = copy.deepcopy(self._defaults['interfaceDefaults'])
        self.data['interfaces'].append(iface)
    
    
    def addRegister(self, regData, ifaceNum=0, ifaceName=None):
        """ Adds a default register to an interface.
        
        This is a used by HWH -> YARD converter.
        """
        self.data['interfaces'][ifaceNum]['registers'].append(regData)
    
    
    def parseAddress(self, reg):
        """ This method parses the user given address value.
        
        This address value can be several formats:
            - <integer> This is the simplest way. The user can place a register into a given address.
                The integer format can be deimal or hexadecimal (starts with '0x')
            - <-1> or None: This indicates automatic register address resolution. YARD can resolve
                addresses. This is the recommended way.
            - value[:stride:<count>[:<increment>]] indicates register-arrays. Value count and
                increment (if exists) must be integers. The value describes the start address, the
                count indicates the size of the register-array. The increment indicates the
                *address-differences* between the consecutive registers.
        """
        
        address = reg['address']
        
        if address is None:
            return
        elif isinstance(address, int):
            reg['parsedAddress']['start'] = address
        elif isinstance(address, str):
            try:
                defaultIncrement = self.getDatawidth()/8
                stridedata = address.split(':')
                stridedata.append(defaultIncrement) # append default increment. This wont be used if the user give the increment
                startAddr = int(float(stridedata[0]))
                if stridedata[1].lower() != 'stride':
                    logging.error('Error during parsing stride address in reg: %s. >stride< keyword exzpected >%s< given', reg['name'], stridedata[1].lower())
                    raise Exception()
                count = util.toInt(stridedata[2])
                increment = util.toInt(stridedata[3])
                reg['parsedAddress']['start'] = startAddr
                reg['parsedAddress']['count'] = count
                reg['parsedAddress']['increment'] = increment
            except:
                logging.error('Unhandled exception at ' + reg['name'])
                raise
        else:
            raise Exception('Unreachable code reached...')
            
        reg['parsedAddress']['value'] = self._getAddressValues(reg)
        return
        
    
    def rollOutStride(self):
        """ This method rolls out the stride-registers (aka. register-arrays)
        
        This method will creates *count* number copes of the stride-register. Each copy will get
        different serialNumber.
        
        This is useful when the template/renderjob does not supporst stride-registers natively.
        """
        for iface in self.data['interfaces']:
            for reg in iface['registers']:
                if isinstance(reg['parsedAddress']['value'], list) and len(reg['parsedAddress']['value'])>1:
                    iface['registers'].remove(reg)
                    for i, addressValue in enumerate(reg['parsedAddress']['value']):
                        regSN = copy.deepcopy(reg)
                        regSN['parsedAddress']['value'] = [reg['parsedAddress']['value'][i]]
                        regSN['parsedAddress']['start'] = reg['parsedAddress']['value'][i]
                        regSN['parsedAddress']['count'] = -1
                        regSN['parsedAddress']['increment'] = -1
                        regSN['parsedAddress']['serialNumber'] = i
                        iface['registers'].insert(i, regSN)

        
    def fillAllFields(self, data=None):
        """ fills all fields in raw yard data.
        Some fields are optional during designing a yard register descriptor.
        Some of them can be derived from other fields, others can get its
        default value.
        This method creates a fuly detailed yard structure
        
        Keyword arguments:
        db -- holds the parsed (raw) yard data. Optional, overrides the data
                given to constructor.
        """
        
        if data is not None:
            self.data = data
            
        self.loadDefaults()
        
        for iface in self.data['interfaces']:
            
            for reg in iface['registers']:
                self.dictMrg(reg, self._defaults['registerDefaults'])
                self.parseAddress(reg)
                
                if reg['access'] is not None:
                    if reg['location'] is None:
                        if reg['access'] == 'RW':
                            reg['location'] = 'pif'
                        else:
                            reg['location'] = 'core'
                            
                elif reg['location'] is not None:
                    if reg['access'] is None:
                        if reg['location'] == 'pif':
                            reg['access'] = 'RW'
                        else:
                            reg['access'] = 'RO'
                else:
                    logging.error('Nether location nor access has defined in reg %s', reg['name'])
                    
                if reg['width'] is None:
                    reg['width'] = self.getDatawidth(0)
                if reg['type'] is None:
                    reg['type'] = 'std_logic_vector'
                if reg['hasReadEvent'] is None:
                    reg['hasReadEvent'] = False
                if reg['hasWriteEnable'] is None:
                    if reg['access'] == 'RW' and reg['location'] == 'core':
                        reg['hasWriteEnable'] = True
                    else:
                        reg['hasWriteEnable'] = False
                
                if reg['fields']:
                    for bf in reg['fields']:
                        if bf['access'] == None:
                            bf['access'] = reg['access']
                        try:
                            pos = util.toInt(bf['position'])
                            length = 1
                            start = pos
                        except:
                            pos = str(bf['position']).split(':')
                            posHigh = util.toInt(pos[0])
                            posLow = util.toInt(pos[1])
                            length = posHigh-posLow+1
                            start = posLow
                            
                        bf['_positionLength'] = length
                        bf['_positionStart'] = start
                              
        self.dataDirthy=False
        
        
    def export(self, filename=None):
        """ Exports the state of the Database.
        """
        if filename is None:
            if self.dataDirthy:
                filename = '~' + self.data['name'] + '_dirtyDB.yaml'
            else:
                filename = '~' + self.data['name'] + '_DB.yaml'
                
        filename = os.path.join(self.get_yard_file_folder(), filename)
            
        logging.debug('Exporting to file: %s', filename)
        yaml.Dumper.ignore_aliases = lambda *args : True
        with open(filename, 'w') as f:    
            f.write(yaml.dump(self.data))
           