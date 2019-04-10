<%def name="portDeclaration(renderdata, lastComa)">
    % for i, port in enumerate(renderdata['ports']):
      % if lastComa or (i < len(renderdata['ports'])-1):
        ${port['decoratedName'].ljust(16)} : ${port['dir']} ${port['fulltype']};
      % else:
        ${port['decoratedName'].ljust(16)} : ${port['dir']} ${port['fulltype']}
      % endif
    % endfor    
</%def>

<%def name="signalDeclaration(signals)">
    % for sig in signals:
      % if sig['defaultValue'] is None :
        signal ${sig['decoratedName'].ljust(16)} : ${sig['fulltype']};
      % else:
        signal ${sig['decoratedName'].ljust(16)} : ${sig['fulltype']} := ${sig['defaultValue']};
      % endif
    % endfor   
</%def>

<%def name="portAssignments(assignmentsPairs, lastComa)">
    % for i, (port, sig) in enumerate(assignmentsPairs):
      % if lastComa or (i < len(assignmentsPairs)-1):
        ${port['decoratedName'].ljust(16)} => ${sig['decoratedName']},
      % else:
        ${port['decoratedName'].ljust(16)} => ${sig['decoratedName']}
      % endif
    % endfor   
</%def>

<%def name="axiLitePortAssignments(lastComa)">
    s_axi_aclk      => s_axi_aclk,
    s_axi_aresetn   => s_axi_aresetn,
    s_axi_awaddr    => s_axi_awaddr,
    s_axi_awprot    => s_axi_awprot,
    s_axi_awvalid   => s_axi_awvalid,
    s_axi_awready   => s_axi_awready,
    s_axi_wdata     => s_axi_wdata,
    s_axi_wstrb     => s_axi_wstrb,
    s_axi_wvalid    => s_axi_wvalid,
    s_axi_wready    => s_axi_wready,
    s_axi_bresp     => s_axi_bresp,
    s_axi_bvalid    => s_axi_bvalid,
    s_axi_bready    => s_axi_bready,
    s_axi_araddr    => s_axi_araddr,
    s_axi_arprot    => s_axi_arprot,
    s_axi_arvalid   => s_axi_arvalid,
    s_axi_arready   => s_axi_arready,
    s_axi_rdata     => s_axi_rdata,
    s_axi_rresp     => s_axi_rresp,
    s_axi_rvalid    => s_axi_rvalid,
    % if lastComa:
      s_axi_rready    => s_axi_rready,
    % else:
      s_axi_rready    => s_axi_rready
    % endif
</%def>

<%def name="axiLitePortDeclaration(lastComa)">
    s_axi_aclk      => s_axi_aclk,
    s_axi_aresetn   => s_axi_aresetn,
    s_axi_awaddr    => s_axi_awaddr,
    s_axi_awprot    => s_axi_awprot,
    s_axi_awvalid   => s_axi_awvalid,
    s_axi_awready   => s_axi_awready,
    s_axi_wdata     => s_axi_wdata,
    s_axi_wstrb     => s_axi_wstrb,
    s_axi_wvalid    => s_axi_wvalid,
    s_axi_wready    => s_axi_wready,
    s_axi_bresp     => s_axi_bresp,
    s_axi_bvalid    => s_axi_bvalid,
    s_axi_bready    => s_axi_bready,
    s_axi_araddr    => s_axi_araddr,
    s_axi_arprot    => s_axi_arprot,
    s_axi_arvalid   => s_axi_arvalid,
    s_axi_arready   => s_axi_arready,
    s_axi_rdata     => s_axi_rdata,
    s_axi_rresp     => s_axi_rresp,
    s_axi_rvalid    => s_axi_rvalid,
    % if lastComa:
      s_axi_rready    => s_axi_rready,
    % else:
      s_axi_rready    => s_axi_rready
    % endif
</%def>