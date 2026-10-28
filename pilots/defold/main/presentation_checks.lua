-- Tests the real instantiated rigid-part objects, not a second animation model.
local Layout=require 'main.layout'
local M={}
function M.run(self)
 local n=0
 local function check(ok,label)n=n+1;assert(ok,label)end
 check(Layout.width==1280 and Layout.height==720,'landscape reference canvas')
 check(Layout.right-Layout.left==992 and Layout.top-Layout.bottom==528,'one bounded arena viewport')
 check(not Layout.field(72,340)and not Layout.field(1208,340),'left and right controls cannot walk or aim')
 check(Layout.field(640,350),'field remains interactive')
 check(self.hero_parts.leg_l~=nil and self.hero_parts.leg_r~=nil and self.hero_parts.arm_l~=nil and self.hero_parts.arm_r~=nil,'actual articulated body parts instantiated')
 for _,id in pairs(self.hero_parts)do check(go.get_parent(id)==self.hero,'real limb parent is selected hero')end
 local l,r=go.get_rotation(self.hero_parts.leg_l),go.get_rotation(self.hero_parts.leg_r)
 check(math.abs(l.x)>.01 and l.x*r.x<0,'actual walk moves opposite legs')
 check(#self.rigs.dragon==8 and #self.rigs.fox==6,'dragon and fox have independent articulated parts')
 check(self.projectile_nodes~=nil and self.halo_nodes~=nil and self.trails~=nil,'native depth-tested effect state exists')
 return n
end
return M
