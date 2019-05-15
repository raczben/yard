source regutil.tcl

namespace eval ${commondata['name']} {
% for addrDef in commondata['addressDefines']:
  variable ${addrDef['addressDefineName']} ${addrDef['address']}
% endfor
}

% for reg in commondata['registers']:
    % if reg['setter'] is not None:
        proc ${reg['setter']['functionName']} { baseAddr data } {
            wr_reg $baseAddr $::${commondata['name']}::${reg['addressDefineName']} $data
        }
    % endif
    
    % if reg['getter'] is not None:
        proc ${reg['getter']['functionName']} { baseAddr } {
            return [rd_reg $baseAddr $::${commondata['name']}::${reg['addressDefineName']}]
    }
    % endif
    
    % for bf in reg['bitFields']:
        % if bf['setter']:
            proc ${bf['setter']['functionName']} { baseAddr data } {
                wr_reg_bf $baseAddr $::${commondata['name']}::${reg['addressDefineName']} ${bf['start']} ${bf['length']} $data
            }
        % endif
        
        % if bf['getter']:
            proc ${bf['getter']['functionName']} { baseAddr } {
                return [rd_reg_bf $baseAddr $::${commondata['name']}::${reg['addressDefineName']} ${bf['start']} ${bf['length']}]
            }
        % endif
    % endfor
% endfor