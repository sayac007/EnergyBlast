-- Shared display formatting: large earned values stay explicit, never 1e+06.
local F={}
function F.number(value)
 local n=tonumber(value)or 0
 if n~=n or n==math.huge or n==-math.huge then n=0 end
 local digits=string.format('%.0f',math.max(0,math.floor(n)))
 local grouped=digits:reverse():gsub('(%d%d%d)','%1.'):reverse():gsub('^%.','')
 return grouped
end
function F.percent(value)
 return tostring(math.floor(math.max(0,math.min(1,value or 0))*100+.5))..'%'
end
function F.decimal(value)
 local n=tonumber(value)or 0
 if n~=n or n==math.huge or n==-math.huge then n=0 end
 if math.abs(n-math.floor(n+.5))<.00001 then return F.number(n)end
 return string.format('%.1f',math.max(0,n)):gsub('%.',',')
end
return F
