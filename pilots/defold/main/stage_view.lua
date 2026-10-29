-- The portrait uses the same camera-facing hero quad as the battlefield.
-- Share these matrices with native bounds checks so a larger hero's head can
-- never silently move outside the stage while the field still looks correct.
local S={left=30,bottom=290,width=530,height=320}
function S.matrices(w,h,hero,scale)
 local size=math.max(1,math.min(1.75,scale or 1));local growth=size-1
 -- Original quad: foot(0,0,0), head(0,1.26,-1.68). Its centre moves
 -- (.63,-.84) per scale unit. Preserve the original scale-one composition.
 local target=vmath.vector3(hero[1],.5+.63*growth,hero[2]-.8-.84*growth)
 local eye=target+vmath.vector3(0,24,18)
 local view=vmath.matrix4_look_at(eye,target,vmath.vector3(0,1,0))
 local span=1.48*(1+growth*.6)
 local aspect=(w*S.width/1280)/(h*S.height/720)
 local projection=vmath.matrix4_orthographic(-span*aspect,span*aspect,-span,span,.1,100)
 return view,projection,span
end
return S
