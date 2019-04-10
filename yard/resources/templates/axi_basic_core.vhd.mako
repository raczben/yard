<%!
  from yard.renderhelper  import fmt_comment
%>
<%namespace name="util" file="util.vhd.mako"/>
${fmt_comment(lic)}


library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

---------------------------------------------------------------------------------------------------

entity ${renderdata['entityName']} is
  generic (
      -- Width of S_AXI data bus
      g_s_axi_data_width  : integer   := ${renderdata['dataWidth']}
  );
  port (
    -- Global Clock Signal
    s_axi_aclk        : in std_logic;
    s_axi_wdata       : in std_logic_vector(g_s_axi_data_width-1 downto 0);
    
    --------------------------------------------------------------------------------------------
    --
    -- Signals from/to pif 
    --
    --------------------------------------------------------------------------------------------
    ${util.portDeclaration(renderdata=renderdata, lastComa=False)}
     
    );
end ${renderdata['entityName']};

architecture behavioral of ${renderdata['entityName']} is

    --------------------------------------------------
    -- Signals between PIF and CORE
    --------------------------------------------------
    ${util.signalDeclaration(signals=renderdata['signals'])}
    
begin

    % for item in renderdata['writeRegisters']:
      <%
        reg = item['register']
        writeEn = item['writeEn']
      %>
      process (s_axi_aclk)
      begin
        if rising_edge(s_axi_aclk) then 
          % if reg['resetValue'] is not None:
            -- Reset
            if s_axi_aresetn = '0' then
              ${reg['decoratedName']} <= ${reg['resetValue']};
            else    -- s_axi_aresetn = '0'
          % endif
            if (${writeEn['decoratedName']} = '1') then
              ${reg['decoratedName']} <= s_axi_wdata;
            end if;
          % if reg['resetValue'] is not None:
            end if;
          % endif
        end if;
      end process;
    % endfor
    
    
    
end behavioral;