library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;
--use IEEE.STD_LOGIC_arith.all;
--
entity TOmultiplier_p887_p193_m419 is
    port (
      x : in std_logic_vector (7 downto 0);
      xC1,xC2,xC3 : out std_logic_vector (23 downto 0)
    );
end TOmultiplier_p887_p193_m419;
--
architecture struct of TOmultiplier_p887_p193_m419 is
    -- signal declarations
    signal t0,R1,R2,R3,p,Zero: signed(32 downto 0):=(others => '0');
    function SignN(s : std_logic; n : integer) return signed is
        variable Zeros : signed(n-1 downto 0) := (others => '0');
        variable Ones : signed(n-1 downto 0) := (others => '1');
    begin
        if s='1' then
            return Ones;
        else
            return Zeros;
        end if;
    end SignN;
begin -- struct
    -- signal assignments
    p <= signed(SignN(x(7),25)& signed(x(7 downto 0))); -- p = x: adjust length of x
    --     t0 = (x << 7)+x;
    t0 <= shift_left(p,7)
    +shift_left(p,0);
    --     xC1 = (x << 9)+(x << 8)+(x << 7)-(x << 4)+(x << 3)-x;
    R1 <= shift_left(p,9)
    +shift_left(p,8)
    +shift_left(p,7)
    -shift_left(p,4)
    +shift_left(p,3)
    -shift_left(p,0);
    --     xC2 = t0+(x << 6);
    R2 <= t0
    +shift_left(p,6);
    --     xC3 = -((x << 8)+t0+(x << 5)+(x << 1));
    R3 <= shift_left(p,8)
    +t0
    +shift_left(p,5)
    +shift_left(p,1);
    -- take the least significant bits of Ri:
    xC1 <= std_logic_vector(R1(23 downto 0));
    xC2 <= std_logic_vector(R2(23 downto 0));
    xC3 <= std_logic_vector(-R3(23 downto 0));
end struct;
-- Number of adders: 10
library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;
--use IEEE.STD_LOGIC_arith.all;
--
entity TOmultiplier_p0_p908_p418 is
    port (
      x : in std_logic_vector (7 downto 0);
      xC1,xC2,xC3 : out std_logic_vector (23 downto 0)
    );
end TOmultiplier_p0_p908_p418;
--
architecture struct of TOmultiplier_p0_p908_p418 is
    -- signal declarations
    signal R1,R2,R3,p,Zero: signed(32 downto 0):=(others => '0');
    function SignN(s : std_logic; n : integer) return signed is
        variable Zeros : signed(n-1 downto 0) := (others => '0');
        variable Ones : signed(n-1 downto 0) := (others => '1');
    begin
        if s='1' then
            return Ones;
        else
            return Zeros;
        end if;
    end SignN;
begin -- struct
    -- signal assignments
    p <= signed(SignN(x(7),25)& signed(x(7 downto 0))); -- p = x: adjust length of x
    --     xC1=Zero;
    R1 <= Zero;
    --     xC2=(x<<10)-(x<<7)+(x<<3)+(x<<2);
    R2 <= shift_left(p,10)
    -shift_left(p,7)
    +shift_left(p,3)
    +shift_left(p,2);
    --     xC3=(x<<8)+(x<<7)+(x<<5)+(x<<1);
    R3 <= shift_left(p,8)
    +shift_left(p,7)
    +shift_left(p,5)
    +shift_left(p,1);
    -- take the least significant bits of Ri:
    xC1 <= std_logic_vector(R1(23 downto 0));
    xC2 <= std_logic_vector(R2(23 downto 0));
    xC3 <= std_logic_vector(R3(23 downto 0));
end struct;
-- Number of adders: 6
library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;
--use IEEE.STD_LOGIC_arith.all;
--
entity TOmultiplier_p461_m371_p806 is
    port (
      x : in std_logic_vector (7 downto 0);
      xC1,xC2,xC3 : out std_logic_vector (23 downto 0)
    );
end TOmultiplier_p461_m371_p806;
--
architecture struct of TOmultiplier_p461_m371_p806 is
    -- signal declarations
    signal t0,t1,R1,R2,R3,p,Zero: signed(32 downto 0):=(others => '0');
    function SignN(s : std_logic; n : integer) return signed is
        variable Zeros : signed(n-1 downto 0) := (others => '0');
        variable Ones : signed(n-1 downto 0) := (others => '1');
    begin
        if s='1' then
            return Ones;
        else
            return Zeros;
        end if;
    end SignN;
begin -- struct
    -- signal assignments
    p <= signed(SignN(x(7),25)& signed(x(7 downto 0))); -- p = x: adjust length of x
    --     t0 = (x << 8)+(x << 1);
    t0 <= shift_left(p,8)
    +shift_left(p,1);
    --     t1 = (x << 9)+(x << 2);
    t1 <= shift_left(p,9)
    +shift_left(p,2);
    --     xC1 = t1-(x << 6)+(x << 3)+x;
    R1 <= t1
    -shift_left(p,6)
    +shift_left(p,3)
    +shift_left(p,0);
    --     xC2 = -(t0+(x << 7)-(x << 4)+x);
    R2 <= t0
    +shift_left(p,7)
    -shift_left(p,4)
    +shift_left(p,0);
    --     xC3 = t1+t0+(x << 5);
    R3 <= t1
    +t0
    +shift_left(p,5);
    -- take the least significant bits of Ri:
    xC1 <= std_logic_vector(R1(23 downto 0));
    xC2 <= std_logic_vector(-R2(23 downto 0));
    xC3 <= std_logic_vector(R3(23 downto 0));
end struct;
-- Number of adders: 10
    library IEEE;
    use IEEE.STD_LOGIC_1164.all;
    use IEEE.NUMERIC_STD.all;
    --
    entity MatrixMult is
      port (
        x,y,z : in std_logic_vector (7 downto 0);
        R1,R2,R3 : out std_logic_vector (23 downto 0)
      );
    end MatrixMult;
    architecture struct of MatrixMult is
    -- component declaration(s):
      component TOmultiplier_p887_p193_m419 is
        port (
          x : in std_logic_vector (7 downto 0);
          xC1,xC2,xC3 : out std_logic_vector (23 downto 0)
        );
      end component TOmultiplier_p887_p193_m419;
      component TOmultiplier_p0_p908_p418 is
        port (
          x : in std_logic_vector (7 downto 0);
          xC1,xC2,xC3 : out std_logic_vector (23 downto 0)
        );
      end component TOmultiplier_p0_p908_p418;
      component TOmultiplier_p461_m371_p806 is
        port (
          x : in std_logic_vector (7 downto 0);
          xC1,xC2,xC3 : out std_logic_vector (23 downto 0)
        );
      end component TOmultiplier_p461_m371_p806;
      -- signal declarations:
      signal xC1,xC2,xC3 : std_logic_vector (23 downto 0); -- outputs
      signal yB1,yB2,yB3 : std_logic_vector (23 downto 0); -- outputs
      signal zA1,zA2,zA3 : std_logic_vector (23 downto 0); -- outputs
      signal Zero : signed(23 downto 0):=(others => '0');
      begin -- struct
      -- connecting signals to multipliers:
      M1: TOmultiplier_p887_p193_m419 port map (x, xC1,xC2,xC3);
      M2: TOmultiplier_p0_p908_p418 port map (y, yB1,yB2,yB3);
      M3: TOmultiplier_p461_m371_p806 port map (z, zA1,zA2,zA3);
      -- adders for dot products:
          -- constants: 887,0,461
      R1 <= std_logic_vector(signed(xC1)+signed(zA1));
          -- constants: 193,908,371
      R2 <= std_logic_vector(signed(xC2)+signed(yB2)+signed(zA2));
          -- constants: 419,418,806
      R3 <= std_logic_vector(signed(xC3)+signed(yB3)+signed(zA3));
    end struct;