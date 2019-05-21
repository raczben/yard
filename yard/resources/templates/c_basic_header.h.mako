#ifndef ${commondata['headerGuardDefine']}
#define ${commondata['headerGuardDefine']}

#define __DTYPE_32__

#include "regutil.h"
#include "${commondata['headerName']}"

% for reg in commondata['registers']:
    #define ${reg['addressDefineName']} ${hex(reg['addressDefineValue'])}
    % for bf in reg['bitFields']:
        #define ${bf['addressDefineName']} ${hex(bf['addressDefineValue'])}
    % endfor
% endfor


% for reg in commondata['registers']:
    % if reg['setter'] is not None:
        void ${reg['setter']['functionName']}(${commondata['addressType']} baseAddr, ${commondata['dataType']} data);
    % endif
    \
    % if reg['setter'] is not None:
        void ${reg['setter']['functionName']}(${commondata['addressType']} baseAddr, int ch, ${commondata['dataType']} data);
    % endif
    \
    % if reg['getter'] is not None:
    ${commondata['dataType']} ${reg['getter']['functionName']}(${commondata['addressType']} baseAddr);
    % endif
    \
    % for bf in reg['bitFields']:
        % if bf['implementSet']:
            void set_${reg['name']}_${bf['name']}_bf(${commondata['addressType']} baseAddr, ${commondata['dataType']} data);
        % endif
        
        % if bf['implementGet']:
            ${commondata['dataType']} get_${reg['name']}_${bf['name']}_bf(${commondata['addressType']} baseAddr);
        % endif
    % endfor
% endfor

#endif // ${commondata['headerGuardDefine']}