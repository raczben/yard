<%!
  from yard.renderhelper  import fmt_comment, decorateVHDLHex, fmt_list
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
        -- Parsed registers
        --
        --------------------------------------------------------------------------------------------
        % for port in renderdata['ports']:
            ${port['decoratedName'].ljust(16)} : ${port['dir']} ${port['fulltype']};
        % endfor
        
        --------------------------------------------------------------------------------------------
        --
        -- AXI-Lite signals for regiser interface
        --
        --------------------------------------------------------------------------------------------
        -- Do not modify the ports beyond this line
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

architecture behavioral of ${renderdata['entityName']} is

    -- AXI4LITE signals
    signal q_axi_awaddr         : std_logic_vector(g_s_axi_addr_width-1 downto 0);
    signal q_axi_awready        : std_logic;
    signal q_axi_wready         : std_logic;
    signal q_axi_bresp          : std_logic_vector(1 downto 0);
    signal q_axi_bvalid         : std_logic;
    signal q_axi_araddr         : std_logic_vector(g_s_axi_addr_width-1 downto 0);
    signal q_axi_arready        : std_logic;
    signal q_axi_rdata          : std_logic_vector(g_s_axi_data_width-1 downto 0);
    signal q_axi_rresp          : std_logic_vector(1 downto 0);
    signal q_axi_rvalid         : std_logic;
    
    signal c_slv_reg_rden       : std_logic;
    signal c_slv_reg_wren       : std_logic;
    signal c_reg_data_out       : std_logic_vector(g_s_axi_data_width-1 downto 0);
    signal byte_index           : integer;
    signal q_aw_en              : std_logic;

    --------------------------------------------------
    -- AXI REGISTERS
    --------------------------------------------------
    ${util.signalDeclaration(signals=renderdata['signals'])}
    
begin


    -- I/O Connections assignments
    s_axi_awready <= q_axi_awready;
    s_axi_wready  <= q_axi_wready;
    s_axi_bresp   <= q_axi_bresp;
    s_axi_bvalid  <= q_axi_bvalid;
    s_axi_arready <= q_axi_arready;
    s_axi_rdata   <= q_axi_rdata;
    s_axi_rresp   <= q_axi_rresp;
    s_axi_rvalid  <= q_axi_rvalid;
    -- Implement q_axi_awready generation
    -- q_axi_awready is asserted for one s_axi_aclk clock cycle when both
    -- s_axi_awvalid and s_axi_wvalid are asserted. q_axi_awready is
    -- de-asserted when reset is low.

    process (s_axi_aclk)
    begin
      if rising_edge(s_axi_aclk) then 
        if s_axi_aresetn = '0' then
          q_axi_awready <= '0';
          q_aw_en <= '1';
        else
          if (q_axi_awready = '0' and s_axi_awvalid = '1' and s_axi_wvalid = '1' and q_aw_en = '1') then
            -- slave is ready to accept write address when
            -- there is a valid write address and write data
            -- on the write address and data bus. This design 
            -- expects no outstanding transactions. 
            q_axi_awready <= '1';
            elsif (s_axi_bready = '1' and q_axi_bvalid = '1') then
                q_aw_en <= '1';
                q_axi_awready <= '0';
          else
            q_axi_awready <= '0';
          end if;
        end if;
      end if;
    end process;

    -- Implement q_axi_awaddr latching
    -- This process is used to latch the address when both 
    -- s_axi_awvalid and s_axi_wvalid are valid. 

    process (s_axi_aclk)
    begin
      if rising_edge(s_axi_aclk) then 
        if s_axi_aresetn = '0' then
          q_axi_awaddr <= (others => '0');
        else
          if (q_axi_awready = '0' and s_axi_awvalid = '1' and s_axi_wvalid = '1' and q_aw_en = '1') then
            -- Write Address latching
            q_axi_awaddr <= s_axi_awaddr;
          end if;
        end if;
      end if;                   
    end process; 

    -- Implement q_axi_wready generation
    -- q_axi_wready is asserted for one s_axi_aclk clock cycle when both
    -- s_axi_awvalid and s_axi_wvalid are asserted. q_axi_wready is 
    -- de-asserted when reset is low. 

    process (s_axi_aclk)
    begin
      if rising_edge(s_axi_aclk) then 
        if s_axi_aresetn = '0' then
          q_axi_wready <= '0';
        else
          if (q_axi_wready = '0' and s_axi_wvalid = '1' and s_axi_awvalid = '1' and q_aw_en = '1') then
              -- slave is ready to accept write data when 
              -- there is a valid write address and write data
              -- on the write address and data bus. This design 
              -- expects no outstanding transactions.           
              q_axi_wready <= '1';
          else
            q_axi_wready <= '0';
          end if;
        end if;
      end if;
    end process; 

    -- Implement memory mapped register select and write logic generation
    -- The write data is accepted and written to memory mapped registers when
    -- q_axi_awready, s_axi_wvalid, q_axi_wready and s_axi_wvalid are asserted. Write strobes are used to
    -- select byte enables of slave registers while writing.
    -- These registers are cleared when reset (active low) is applied.
    -- Slave register write enable is asserted when valid address and data are available
    -- and the slave is ready to accept the write address and write data.
    c_slv_reg_wren <= q_axi_wready and s_axi_wvalid and q_axi_awready and s_axi_awvalid ;

    proc_reg_writer:
    process (s_axi_aclk)
    begin
      if rising_edge(s_axi_aclk) then 
        -- Reset non-Read-only registers, which are resetable.
        if s_axi_aresetn = '0' then
          % for reg in renderdata['writeRegisters']:
            % if reg['resetValue'] is not None:
              ${reg['decoratedName']} <= std_logic_vector(to_unsigned(${decorateVHDLHex(reg['resetValue'])}, ${reg['width']}));
            % endif
          % endfor
        else    -- s_axi_aresetn = '0'
          if (c_slv_reg_wren = '1') then
            -- Select the register
            case to_integer(unsigned(q_axi_awaddr)) is
              % for reg in renderdata['writeRegisters']:
                when ${decorateVHDLHex(reg['addressInBytes'])} =>
                for byte_index in 0 to (g_s_axi_data_width/8-1) loop
                  if ( s_axi_wstrb(byte_index) = '1' ) then
                    ${reg['decoratedName']}(byte_index*8+7 downto byte_index*8) <= s_axi_wdata(byte_index*8+7 downto byte_index*8);
                  end if;
                end loop;
              % endfor
            when others =>
            end case;  -- Select the register
          end if; -- c_slv_reg_wren = '1'
        end if; -- s_axi_aresetn /= '0'
      end if;  -- rising_edge(s_axi_aclk)               
    end process; 
   

    -- Implement write response logic generation
    -- The write response and response valid signals are asserted by the slave 
    -- when q_axi_wready, s_axi_wvalid, q_axi_wready and s_axi_wvalid are asserted.  
    -- This marks the acceptance of address and indicates the status of 
    -- write transaction.

    process (s_axi_aclk)
    begin
      if rising_edge(s_axi_aclk) then 
        if s_axi_aresetn = '0' then
          q_axi_bvalid  <= '0';
          q_axi_bresp   <= "00"; --need to work more on the responses
        else
          if (q_axi_awready = '1' and s_axi_awvalid = '1' and q_axi_wready = '1' and s_axi_wvalid = '1' and q_axi_bvalid = '0'  ) then
            q_axi_bvalid <= '1';
            q_axi_bresp  <= "00"; 
          elsif (s_axi_bready = '1' and q_axi_bvalid = '1') then   --check if bready is asserted while bvalid is high)
            q_axi_bvalid <= '0';                                 -- (there is a possibility that bready is always asserted high)
          end if;
        end if;
      end if;                   
    end process; 

    -- Implement q_axi_arready generation
    -- q_axi_arready is asserted for one s_axi_aclk clock cycle when
    -- s_axi_arvalid is asserted. q_axi_awready is 
    -- de-asserted when reset (active low) is asserted. 
    -- The read address is also latched when s_axi_arvalid is 
    -- asserted. q_axi_araddr is reset to zero on reset assertion.

    process (s_axi_aclk)
    begin
      if rising_edge(s_axi_aclk) then 
        if s_axi_aresetn = '0' then
          q_axi_arready <= '0';
          q_axi_araddr  <= (others => '1');
        else
          if (q_axi_arready = '0' and s_axi_arvalid = '1') then
            -- indicates that the slave has acceped the valid read address
            q_axi_arready <= '1';
            -- Read Address latching 
            q_axi_araddr  <= s_axi_araddr;           
          else
            q_axi_arready <= '0';
          end if;
        end if;
      end if;                   
    end process; 

    -- Implement axi_arvalid generation
    -- q_axi_rvalid is asserted for one s_axi_aclk clock cycle when both 
    -- s_axi_arvalid and q_axi_arready are asserted. The slave registers 
    -- data are available on the q_axi_rdata bus at this instance. The 
    -- assertion of q_axi_rvalid marks the validity of read data on the 
    -- bus and q_axi_rresp indicates the status of read transaction.q_axi_rvalid 
    -- is deasserted on reset (active low). q_axi_rresp and q_axi_rdata are 
    -- cleared to zero on reset (active low).  
    process (s_axi_aclk)
    begin
      if rising_edge(s_axi_aclk) then
        if s_axi_aresetn = '0' then
          q_axi_rvalid <= '0';
          q_axi_rresp  <= "00";
        else
          if (q_axi_arready = '1' and s_axi_arvalid = '1' and q_axi_rvalid = '0') then
            -- Valid read data is available at the read data bus
            q_axi_rvalid <= '1';
            q_axi_rresp  <= "00"; -- 'OKAY' response
          elsif (q_axi_rvalid = '1' and s_axi_rready = '1') then
            -- Read data is accepted by the master
            q_axi_rvalid <= '0';
          end if;            
        end if;
      end if;
    end process;

    -- Implement memory mapped register select and read logic generation
    -- Slave register read enable is asserted when valid address is available
    -- and the slave is ready to accept the read address.
    c_slv_reg_rden <= q_axi_arready and s_axi_arvalid and (not q_axi_rvalid) ;


    process ( ${fmt_list([x['decoratedName'] for x in renderdata['readRegisters']], commondata['pageWidth'])} )
    begin
      -- Select the register
      case to_integer(unsigned(q_axi_araddr)) is
        % for reg in renderdata['readRegisters']:
          when ${decorateVHDLHex(reg['addressInBytes'])} =>
            c_reg_data_out  <= ${reg['decoratedName']};
        % endfor
      when others =>
          c_reg_data_out  <= (others => '0');
      end case;
    end process;
    
    % if len(renderdata) > 0:
      -- Folowing signals are active when master reads the given register.
      % for sig in renderdata['readEvents']:
        ${sig['decoratedName']} <= '1' when c_slv_reg_rden = '1' and to_integer(unsigned(q_axi_araddr)) = ${decorateVHDLHex(reg['addressInBytes'])} else '0';
      % endfor
    % endif

    -- Output register or memory read data
    process( s_axi_aclk ) is
    begin
      if (rising_edge (s_axi_aclk)) then
        if ( s_axi_aresetn = '0' ) then
          q_axi_rdata  <= (others => '0');
        else
          if (c_slv_reg_rden = '1') then
            -- When there is a valid read address (s_axi_arvalid) with 
            -- acceptance of read address by the slave (q_axi_arready), 
            -- output the read dada 
            -- Read address mux
              q_axi_rdata <= c_reg_data_out;     -- register read data
          end if;   
        end if;
      end if;
    end process;
    
    --
    -- Port assignments
    --
    % for asn in renderdata['IOAssignments']:
      ${asn['left']['decoratedName'].ljust(16)} <= ${asn['right']['decoratedName']};
    % endfor
    
end behavioral;