-- Logical 720x1280 safe zones. No interactive HUD node enters the scene viewport.
local L={width=720,height=1280,bottom=260,top=1100}
L.controls={menu={650,1235,74,64},sound={555,1235,84,64},fire={610,100,148,148},dash={110,100,140,140},hint={350,184,190,48},radio={350,120,180,48},gear={350,54,180,48}}
function L.field(x,y)return x>=0 and x<=L.width and y>L.bottom and y<L.top end
function L.safe(x,y,w,h)return y+h/2<=L.bottom or y-h/2>=L.top end
return L
