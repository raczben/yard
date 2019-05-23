#include "${commondata['headerName']}"
#include "regutil.h"


% for reg in commondata['registers']:
    % if reg['setter'] is not None:
        % if reg['addressIncrement'] < 0:
            void ${reg['setter']['functionName']}(${commondata['addressType']} baseAddr, ${commondata['dataType']} data){
                WRITE_REG(baseAddr, ${reg['addressDefineName']}, data);
            }
        % else :
            void ${reg['setter']['functionName']}(${commondata['addressType']} baseAddr, int ch, ${commondata['dataType']} data) {
                WRITE_REG(baseAddr + ch * reg['addressIncrement'], ${reg['addressDefineName']}, data);
            }
        % endif
    % endif
    
    % if reg['getter'] is not None:
        % if reg['addressIncrement'] < 0:
            ${commondata['dataType']} ${reg['getter']['functionName']}(${commondata['addressType']} baseAddr){
                return READ_REG(baseAddr, ${reg['addressDefineName']});
            }
        % else :
            ${commondata['dataType']} ${reg['getter']['functionName']}(${commondata['addressType']} baseAddr, int ch){
                return READ_REG(baseAddr + ch * reg['addressIncrement'], ${reg['addressDefineName']});
            }
        % endif
    % endif
    
    % for bf in reg['bitFields']:
        % if bf['implementSet']:
            % if reg['addressIncrement'] < 0:
                void set_${reg['name']}_${bf['name']}_bf(${commondata['addressType']} baseAddr, ${commondata['dataType']} data){
                    WRITE_REG_BF(baseAddr, ${reg['addressDefineName']}, bf['start'], bf['len'], data);
                }
            $ else:
                void set_${reg['name']}_${bf['name']}_bf(${commondata['addressType']} baseAddr, int ch, ${commondata['dataType']} data){
                    WRITE_REG_BF(baseAddr + ch * reg['addressIncrement'], ${reg['addressDefineName']}, bf['start'], bf['len'], data);
                }
            % endif
        % endif
        
        % if bf['implementSet']:
            % if reg['addressIncrement'] < 0:
                ${commondata['dataType']} get_${reg['name']}_${bf['name']}_bf(${commondata['addressType']} baseAddr){
                    return READ_REG_BF(baseAddr, ${reg['addressDefineName']}, bf['start'], bf['len']);
                }
            $ else:
                ${commondata['dataType']} get_${reg['name']}_${bf['name']}_bf(${commondata['addressType']} baseAddr, int ch){
                    return READ_REG_BF(baseAddr + ch * reg['addressIncrement'], ${reg['addressDefineName']}, bf['start'], bf['len']);
                }
            % endif
        % endif
    % endfor
% endfor
