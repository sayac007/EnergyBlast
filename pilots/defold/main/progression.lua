-- Lifetime score never falls. The shop spends a separate, derived star balance.
local P={}
function P.bind(g)
 function g:wallet()local n=self:total();for id,price in pairs(self.saved.spent or{})do n=n-price end;return math.max(0,n)end
 function g:owns(id)
  if not self.data.shop_enabled then
   for _,u in ipairs(self.data.unlocks)do if u.id==id then return self:total()>=u.stars end end;return false
  end
  return(self.saved.purchases or{})[id]==true
 end
 function g:buy(id)
  for _,u in ipairs(self.data.unlocks)do if u.id==id then
   if self:owns(id)then if id=='prism'then self.saved.weapon=self.saved.weapon=='prism'and'pulse'or'prism';self.changed()end;return false end
   local cost=u.price or u.stars
   if self:wallet()<cost then self.shop_status='Noch '..(cost-self:wallet())..' Sterne';return false end
   self.saved.purchases=self.saved.purchases or{};self.saved.spent=self.saved.spent or{};self.saved.purchases[id]=true;self.saved.spent[id]=cost
   if id=='prism'then self.saved.weapon='prism'end
   if id=='armor'and self.hp then self.max_hp=self.max_hp+1;self.hp=math.min(self.max_hp,self.hp+1)end
   self.shop_status='AUSGERUESTET';self.changed();return true
  end end;return false
 end
 function g:set_character(id)
  for _,c in ipairs(self.data.characters or{})do if c.id==id then self.saved.character=id;self.changed();return true end end;return false
 end
 function g:character()local id=self.saved.character or'hero';for _,c in ipairs(self.data.characters or{})do if c.id==id then return c end end;return{id='hero',name='NOVA',shot='energy'}end
 -- One-time migration preserves gear already granted by pre-shop versions.
 if g.data.shop_enabled and g.saved.schema~=2 then
  g.saved.purchases=g.saved.purchases or{};g.saved.spent={}
  for _,u in ipairs(g.data.unlocks)do if g:total()>=u.stars then g.saved.purchases[u.id]=true end end
  g.saved.schema=2
 end
end
return P
