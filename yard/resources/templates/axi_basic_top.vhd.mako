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
        g_s_axi_data_width  : integer   := ${renderdata['dataWidth']};

        -- Width of S_AXI address bus
        g_s_axi_addr_width  : integer   := ${renderdata['addressWidth']}
        
    );
    port (
        --------------------------------------------------------------------------------------------
        --
        -- AXI-Lite signals for regiser interface
        --
        --------------------------------------------------------------------------------------------
        -- Global Clock Signal
        s_axi_aclk        : in std_logic;
        
        -- Global Reset Signal. This Signal is Active LOW
        s_axi_aresetn     : in std_logic;
        
        -- Write address (issued by master, acceped by Slave)
        s_axi_awaddr      : in std_logic_vector(g_s_axi_addr_width-1 downto 0);
        
        -- Write channel Protection type. This signal indicates the
            -- privilege and security level of the transaction, and whether
            -- the transaction is a data access or an instruction access.
        s_axi_awprot      : in std_logic_vector(2 downto 0);
        
        -- Write address valid. This signal indicates that the master signaling
            -- valid write address and control information.
        s_axi_awvalid     : in std_logic;
        
        -- Write address ready. This signal indicates that the slave is ready
            -- to accept an address and associated control signals.
        s_axi_awready     : out std_logic;
        
        -- Write data (issued by master, acceped by Slave) 
        s_axi_wdata       : in std_logic_vector(g_s_axi_data_width-1 downto 0);
        
        -- Write strobes. This signal indicates which byte lanes hold
            -- valid data. There is one write strobe bit for each eight
            -- bits of the write data bus.    
        s_axi_wstrb       : in std_logic_vector((g_s_axi_data_width/8)-1 downto 0);
        
        -- Write valid. This signal indicates that valid write
            -- data and strobes are available.
        s_axi_wvalid      : in std_logic;
        
        -- Write ready. This signal indicates that the slave
            -- can accept the write data.
        s_axi_wready      : out std_logic;
        
        -- Write response. This signal indicates the status
            -- of the write transaction.
        s_axi_bresp       : out std_logic_vector(1 downto 0);
        
        -- Write response valid. This signal indicates that the channel
            -- is signaling a valid write response.
        s_axi_bvalid      : out std_logic;
        
        -- Response ready. This signal indicates that the master
            -- can accept a write response.
        s_axi_bready      : in std_logic;
        
        -- Read address (issued by master, acceped by Slave)
        s_axi_araddr      : in std_logic_vector(g_s_axi_addr_width-1 downto 0);
        
        -- Protection type. This signal indicates the privilege
            -- and security level of the transaction, and whether the
            -- transaction is a data access or an instruction access.
        s_axi_arprot      : in std_logic_vector(2 downto 0);
        
        -- Read address valid. This signal indicates that the channel
            -- is signaling valid read address and control information.
        s_axi_arvalid     : in std_logic;
        
        -- Read address ready. This signal indicates that the slave is
            -- ready to accept an address and associated control signals.
        s_axi_arready     : out std_logic;
        
        -- Read data (issued by slave)
        s_axi_rdata       : out std_logic_vector(g_s_axi_data_width-1 downto 0);
        
        -- Read response. This signal indicates the status of the
            -- read transfer.
        s_axi_rresp       : out std_logic_vector(1 downto 0);
        
        -- Read valid. This signal indicates that the channel is
            -- signaling the required read data.
        s_axi_rvalid      : out std_logic;
        
        -- Read ready. This signal indicates that the master can
            -- accept the read data and response information.
        s_axi_rready      : in std_logic
        
    );
end ${renderdata['entityName']};

architecture structural of ${renderdata['entityName']} is
    --------------------------------------------------
    -- Signals between PIF and CORE
    --------------------------------------------------
    
    ${util.signalDeclaration(signals=renderdata['signals'])}
    
begin
    

    inst_${renderdata['coreEntityName']} : entity work.${renderdata['coreEntityName']}
    port map (
      s_axi_aclk        => s_axi_aclk,
      s_axi_wdata       => s_axi_wdata,
      
      -- Signals between PIF and CORE
      
      ${util.portAssignments(
        assignmentsPairs=[(x['left'], x['right']) for x in renderdata['corePortAssignments']],
        lastComa=False
        )}

    );


    inst_${renderdata['pifEntityName']} : entity work.${renderdata['pifEntityName']}
      generic map (
      g_s_axi_data_width => g_s_axi_data_width
    )
    port map (
      -- Signals between PIF and CORE
      
      ${util.portAssignments(
        assignmentsPairs=[(x['left'], x['right']) for x in renderdata['pifPortAssignments']],
        lastComa=True
        )}
        
      -- AXI-Lite signals
      ${util.axiLitePortAssignments(lastComa=False)}
    );
    
end structural;