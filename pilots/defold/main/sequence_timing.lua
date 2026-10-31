-- Shared observation timing for every copy of the light-sequence display.
-- Historical fixtures keep their original tempo; the live campaign is slower.
local T={}
local EPSILON=1e-8
function T.state(g)
 local sequence=g.m and g.m.sequence or{}
 local cfg=g.data and g.data.campaign_enabled and g.data.sequence_timing
 local step,lit,cycle,pause=.9,.6,4.6,4.6-#sequence*.9
 if cfg then
  step=cfg.step_seconds;lit=cfg.lit_seconds;pause=cfg.pause_seconds
  cycle=#sequence*step+pause
 end
 local epsilon=cfg and EPSILON or 0
 local phase=(g.sequence_clock or 0)%cycle
 -- Exact boundaries should not change their meaning through decimal rounding.
 if cycle-phase<epsilon then phase=0 end
 local slot=math.floor((phase+epsilon)/step)+1
 local order=sequence[slot]
 local elapsed=cfg and phase-(slot-1)*step or phase%step
 local illuminated=order~=nil and elapsed<lit-epsilon
 return{phase=phase,slot=slot,order=order,lit=illuminated,
  lit_order=illuminated and order or nil,step_seconds=step,lit_seconds=lit,
  cycle_seconds=cycle,pause_seconds=pause}
end
function T.is_lit(g,order)
 local state=T.state(g)
 return state.lit and state.order==order
end
return T
