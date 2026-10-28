-- Tests the actual native model, material frame and foot anchor, not a second animation model.
local Layout=require 'main.layout'
local M={}
function M.run(self)
 local n=0
 local function check(ok,label)n=n+1;assert(ok,label)end
 check(Layout.width==1280 and Layout.height==720,'landscape reference canvas')
 check(Layout.right-Layout.left==992 and Layout.top-Layout.bottom==528,'one bounded arena viewport')
 check(not Layout.field(72,340)and not Layout.field(1208,340),'left and right controls cannot walk or aim')
 check(Layout.field(640,350),'field remains interactive')
 check(self.hero~=nil and #self.hero_ids==1,'selected illustrated actor is a native world object')
 local frame=go.get(msg.url(nil,self.hero,'model'),'frame')
 check(frame.z==4 and frame.w==2,'real model samples the eight-frame directional animation atlas')
 check(frame.x==self.hero_frame and frame.x>0,'walking changes the frame bound to the actual native material')
 check(self.hero_row==0 or self.hero_row==1,'front and rear walking views bounded')
 local p=go.get_position(self.hero)
 check(math.abs(p.x-self.g.p[1])<.001 and math.abs(p.z-self.g.p[2])<.001,'animated drawing stays foot-anchored to actual collider')
 check(go.get_rotation(self.hero).y==0,'camera-facing actor never spins its picture edge-on')
 check(self.projectile_nodes~=nil and self.halo_nodes~=nil and self.trails~=nil,'native depth-tested effect state exists')
 return n
end
return M
