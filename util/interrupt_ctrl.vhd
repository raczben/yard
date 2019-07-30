
library ieee;
use ieee.std_logic_1164.all;

entity interrupt_ctrl is
  generic (
    g_interrupt_width   : integer := 32; -- The width of the interrupt register.
    
    -- g_input_mode specifies the irq type of each bit in i_raw_irq. All bits can be state-sensitive or
    -- edge-sensitive. State-sensitive inputs can be active high ('h') or active low ('l'). Edge-sensitive inputs
    -- can be active at the rising ('r') and the falling ('f') edge.
    -- Example: "rhhh" means a 4 bit width irq input, where the '0' input is active at the rising edge, others are
    -- active high inputs.
    g_input_mode    : string    := "hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"
    
  );
  port (
    i_clk               : in std_logic; -- System clock
    i_rst               : in std_logic; -- Sychronous reset
    
    -- The raw interrupt sources. These input will results the single irq output towards the CPU
    i_raw_irq           : in  std_logic_vector(g_interrupt_width-1 downto 0);
    -- Same as i_raw_irq, readback register of the current state of the interrupts
    o_current_state     : out std_logic_vector(g_interrupt_width-1 downto 0);
    -- Register after the "mode" preproces. (Eg.: active low irqs are inverted)
    o_current_active    : out std_logic_vector(g_interrupt_width-1 downto 0);
    -- The pending register stores the historical preprocessed values of the raw interrupts.
    o_pending           : out std_logic_vector(g_interrupt_width-1 downto 0);
    -- Enalbes/disables each signel interrupt (ANDing the pending)
    i_mask              : in  std_logic_vector(g_interrupt_width-1 downto 0);
    -- The AND-ed pending and mask.
    o_enabled_pending   : out std_logic_vector(g_interrupt_width-1 downto 0);
    
    -- the IRQ signal towards the CPU.
    o_irq               : out std_logic;
    
    -- Clears the full pending register.
    i_clear_all         : in  std_logic;
    -- Clears the corresponding bits in the pending register. (Full '1' sames as i_clear_all)
    i_clear_individual  : in  std_logic_vector(g_interrupt_width-1 downto 0)
  );
end entity;

architecture behavioral of interrupt_ctrl is

    signal q_raw_irq_d1     : std_logic_vector(i_raw_irq'range);
    signal q_raw_irq_d2     : std_logic_vector(i_raw_irq'range);
    signal q_raw_irq_d3     : std_logic_vector(i_raw_irq'range);
    signal q_current_active : std_logic_vector(g_interrupt_width-1 downto 0);
    signal q_pending        : std_logic_vector(g_interrupt_width-1 downto 0);
    signal q_enabled_pending    : std_logic_vector(g_interrupt_width-1 downto 0);
    signal q_irq            : std_logic;

begin

  -- Output assignments:
  o_current_state   <= q_raw_irq_d2;
  o_current_active  <= q_current_active;
  o_pending         <= q_pending;
  o_enabled_pending <= q_enabled_pending;
  o_irq             <= q_irq;
  
  -- Delay of the input for metastability filter and edge detection if its needed.
  proc_input_delay: process (i_clk)
  begin
    if (rising_edge(i_clk)) then
      q_raw_irq_d1 <= i_raw_irq;
      q_raw_irq_d2 <= q_raw_irq_d1;
      q_raw_irq_d3 <= q_raw_irq_d2;
    end if;  -- i_clk      
  end process;
  
  -- Following process does the "preproces" based on the mode generic. It results the q_current_active register.
  proc_current_active: process (i_clk)
  begin
    if (rising_edge(i_clk)) then
      for I in q_raw_irq_d2'low to q_raw_irq_d2'high loop
        case g_input_mode(I+1) is
          when 'h' =>   -- Active high
            q_current_active(I) <= q_raw_irq_d2(I);
          when 'l' =>   -- Active low (Inverter)
            q_current_active(I) <= not q_raw_irq_d2(I);
          when 'r' =>   -- Rising edge
            if q_raw_irq_d2(I) > q_raw_irq_d3(I) then
              q_current_active(I) <= '1';
            else
              q_current_active(I) <= '0';
            end if;
          when 'f' =>   -- Falling edge
            if q_raw_irq_d2(I) < q_raw_irq_d3(I) then
              q_current_active(I) <= '1';
            else
              q_current_active(I) <= '0';
            end if;
          when others =>
            assert False
              report "Unknown letter for mode." severity failure;
        end case;
	  end loop;
    end if;  -- i_clk      
  end process;

  -- Following process stores all active interrupt into the pending register. The pending register can be cleared
  -- using the i_clear_all or i_clear_individual inputs. These inputs should be connected the read/write event of
  -- the pending register in the processor interface. This will results clear-on-read / clear-on-write behaviour.
  --
  -- Tip: If you want to implement a real level sensitive interrupts, with no-pending storage, connect the
  --      corresponding bit in the i_clear_individual '1'.
  proc_pending: process (i_clk)
  begin
    if (rising_edge(i_clk)) then
      if i_clear_all = '1' then
        q_pending <= q_current_active;
      else  -- i_clear_all = '0'  
        for I in q_current_active'low to q_current_active'high loop
          if i_clear_individual(I) = '1' then
            q_pending(I) <= q_current_active(I);
          else  -- i_clear_individual = '0'   
            q_pending(I) <= q_pending(I) OR q_current_active(I);
          end if;   -- i_clear_individual
	    end loop;
      end if;   -- i_clear_all
    end if;  -- i_clk      
  end process;
  
  -- Enabled and pending
  proc_enabled_pending: process (i_clk)
  begin
    if (rising_edge(i_clk)) then
      q_enabled_pending <= q_pending AND i_mask;
    end if;  -- i_clk      
  end process;
  
  -- The interrupt signal towards thw CPU.
  proc_cpu_irq: process (i_clk)
  begin
    if (rising_edge(i_clk)) then
      q_irq <= '0';
      for I in q_enabled_pending'low to q_enabled_pending'high loop
		q_irq <= q_irq OR q_enabled_pending(I);
	  end loop;
    end if;  -- i_clk      
  end process;

end architecture;
