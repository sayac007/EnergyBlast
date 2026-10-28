-- Fixed landscape presentation. Every HUD/control is outside the rendered arena.
local L={width=1280,height=720,left=144,right=1136,bottom=96,top=624}
L.controls={menu={1215,674,88,66},sound={1105,674,92,66},fire={1208,340,126,126},dash={72,340,120,120},hint={72,210,120,70},radio={1208,210,120,70},gear={1208,110,120,64}}
function L.field(x,y)return x>L.left and x<L.right and y>L.bottom and y<L.top end
function L.safe(x,y,w,h)return x+w/2<=L.left or x-w/2>=L.right or y+h/2<=L.bottom or y-h/2>=L.top end
return L
