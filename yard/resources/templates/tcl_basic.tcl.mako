source regutil.tcl


% for addrDef in commondata['addressDefines']:
  set ${addrDef['addressDefineName']} ${addrDef['address']}
% endfor

% for reg in commondata['registers']:
    % if reg['setter'] is not None:
        proc ${reg['setter']['functionName']} { baseAddr data } {
            global ${reg['addressDefineName']}
            wr_reg $baseAddr $${reg['addressDefineName']} $data
        }
    % endif
    
    % if reg['getter'] is not None:
        proc ${reg['getter']['functionName']} { baseAddr } {
            global ${reg['addressDefineName']}
            return [rd_reg $baseAddr $${reg['addressDefineName']}]
    }
    % endif
    
    % for bf in reg['bitFields']:
        % if bf['setter']:
            proc ${bf['setter']['functionName']} { baseAddr data } {
                global ${reg['addressDefineName']}
                wr_reg_bf $baseAddr $${reg['addressDefineName']} ${bf['start']} ${bf['length']} $data
            }
        % endif
        
        % if bf['getter']:
            proc ${bf['getter']['functionName']} { baseAddr } {
                global ${reg['addressDefineName']}
                return [rd_reg_bf $baseAddr $${reg['addressDefineName']} ${bf['start']} ${bf['length']}]
            }
        % endif
    % endfor
% endfor