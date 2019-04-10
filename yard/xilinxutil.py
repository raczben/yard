# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

import util
import main


def getModulesRoot(root):
    """
    Returns the <MODULES> element
    """
    return root.find('MODULES')


def isEqMemRange(mr1, mr2):
    """ Returns true if the two (mr1 and mr2) address ranges have the same base address and high address.
    """
    return mr1 == mr2
    

def isOverlapMemRange(mr1, mr2):
    """ Returns true if the two (mr1, mr2) memory ranges are non disjunct, which means that there is
    one or more address, which are in both ranges. This means address conflict.
    Returns false it the two given address ranges has no common value.
    """
    # Compute intersect:
    intersectStart = max(mr1['baseAddress'], mr2['baseAddress'])
    intersectEnd = min(mr1['highAddress'], mr2['highAddress'])
    
    # overlap, when intesect is non null:
    return intersectStart < intersectEnd


def readHWH(filename):
    """ Reads Xilix's HWH XML file and converts it to YARD database.
    Returns a list of databases. 
    
    Note, that Xilinx HWH and YARD database is a bit different. HWH contains *instances*
    (of a concrete BlockDesign) YARD contains components (aka. modules). Which means YARD is more
    abstract than HWH.
    """
    accessMap = {'read-write': 'RW', 'read-only': 'RO', 'write-only': 'WO'}
    root = ET.parse(filename).getroot()
    
    modules = getModulesRoot(root)
    
    dataBases = []
    globAddrMap = {}
    
    for mod in modules:
        db = main.DataBase()
        dataBases.append(db)
        db.data['name'] = mod.attrib['INSTANCE']
        db.addInterface()
        peripheralPropery={}
        for modParam in mod.findall('./PARAMETERS/PARAMETER'):
            peripheralPropery[modParam.attrib['NAME']] = modParam.attrib['VALUE']
               
        # If this peripheral has a master interface (ie. AXI-Master) there is a list of the slaves
        # connected to this master. Let's store the address ranges (the base addresses) of these
        # slave peripherals.
        # If there is no master interface the following for-loop will bypassed (no iteration)
        for memMap in mod.iter('MEMORYMAP'):
            for mr in memMap.iter('MEMRANGE'):
                instance = mr.attrib['INSTANCE']
                memRange = {}
                memRange['baseAddress'] = util.toInt(mr.attrib['BASEVALUE'])
                memRange['highAddress'] = util.toInt(mr.attrib['HIGHVALUE'])
                if instance in globAddrMap.keys():
                    if not isEqMemRange(globAddrMap[instance], memRange):
                        print('Error: same instance has different address ranges... + ' + instance)
                    continue
                for k, v in globAddrMap.items():
                    if isOverlapMemRange(v, memRange):
                        print('Error: address conflict:  ' + instance + '  ' + k)
                globAddrMap[instance] = memRange
                  
        # Usually a peripheral has registers (connected on its AXI-Slave interface) If it has let's
        # go through these registers and map them, with their field. 
        for reg in mod.findall('.//ADDRESSBLOCKS/ADDRESSBLOCK/REGISTERS/REGISTER'):
            regPropery={}
            regFields={}
            for prop in reg.iter('PROPERTY'):
                regPropery[prop.attrib['NAME']] = prop.attrib['VALUE']
            for bf in reg.findall('FIELDS/FIELD'):
                bfPropery={}
                for prop in reg.iter('PROPERTY'):
                    bfPropery[prop.attrib['NAME']] = prop.attrib['VALUE']
                regFields[bf.attrib['NAME']] = bfPropery
          
            regData = {}
            regData['name'] = reg.attrib['NAME']
            regData['address'] = util.toInt(regPropery['ADDRESS_OFFSET'])
            regData['width'] = util.toInt(regPropery['SIZE'])
            regData['access'] = accessMap[regPropery['ACCESS']]
            regData['brief'] = util.getFirstSentence(regPropery['DESCRIPTION'])
            regData['description'] = regPropery['DESCRIPTION']
            regData['reset'] = util.toInt(regPropery['RESET_VALUE'])
            regData['fields'] = []
            
            # Map the bitfields of the registers.
            for bfName, bf in regFields.items():
                fieldData = {}
                fieldData['name'] = bfName
                fieldData['position'] = '{}:{}'.format(bf['BIT_OFFSET'], bf['BIT_WIDTH'])
                fieldData['description'] = bf['DESCRIPTION']
                fieldData['access'] = accessMap[bf['ACCESS']]
                regData['fields'].append(fieldData)
                
            db.addRegister(regData)
            
    # TODO: this section should be emigrated from here.
    # Prints the base address defines for TCL
    for instance, memrange in globAddrMap.items():
        baseAddr = util.toInt(memrange['baseAddress'])        
        definename = instance.upper() + '_BASE_ADDR'
        print('set ' + definename.ljust(32) + ' ' + hex(baseAddr))     
        
    return dataBases
          

filename = 'D:/work/proj/fpga_top_210401_callisto_bkp_david/bin/ip_subsystem.hwh'
    
for db in readHWH(filename):
    db.export()
    db.fillAllFields()
    db.export()
    gen = main.TCLBaseGenerator(db)
    
    main.logging.info("  Starting generateRenderData...")
    gen.generateRenderData()
    
    gen.exportRenderJobs()
    
    main.logging.info("  Starting render...")
    gen.render()


