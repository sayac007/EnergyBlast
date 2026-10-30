"""Real XTest attack-drone tap/drag, explicit cancel and invalid HUD target.

Selection does not consume stock. Launches fly physically, consume one drone and
kill through the production impact path with real native lightning; hero firing
or walking during these gestures is a failure.
"""
from pathlib import Path
import argparse,tempfile,time
from check_defold_campaign_ui import NativeDriver

def main():
 p=argparse.ArgumentParser();p.add_argument('--engine',type=Path,default=Path('/tmp/energyblast-defold-tools/dmengine'));p.add_argument('--output',type=Path);a=p.parse_args()
 with tempfile.TemporaryDirectory(prefix='energyblast-native-attack-drones-',dir='/tmp')as temporary:
  root=a.output.resolve()if a.output else Path(temporary);root.mkdir(parents=True,exist_ok=True)
  for gesture in ['tap','drag','zoom']:
   with NativeDriver(a.engine,root/gesture,mode='drone_'+gesture)as d:
    d.wait('DEFOLD CAMPAIGN MENU PAGE 1');d.choose(2)
    badge=d.coords('DEFOLD CAMPAIGN DRONE BADGE')
    # Cancelling an actually opened catalogue keeps stock intact.
    before=len(d.text());d.click(*badge);d.coords('DEFOLD CAMPAIGN DRONE OPTION',before)
    cancel=d.coords('DEFOLD CAMPAIGN DRONE CANCEL',before);d.capture('catalogue',a.output is not None);d.click(*cancel)
    d.wait('DEFOLD CAMPAIGN DRONE CANCEL PASS stock=3 shots=0 path=0',before)
    before=len(d.text());d.click(*badge);option=d.coords('DEFOLD CAMPAIGN DRONE OPTION',before)
    before=len(d.text());selection_start=before;d.click(*option)
    d.coords('DEFOLD CAMPAIGN DRONE PREVIEW',before);d.capture('target-preview',a.output is not None)
    # FEUER is a HUD control, never a valid attack-drone drop/target.
    before=len(d.text());d.click(1208,360);d.wait('DEFOLD CAMPAIGN ACTION fire mission=2',before)
    d.wait('DEFOLD CAMPAIGN DRONE SELECTION SAFE mode=target stock=3 shots=0 path=0',before)
    # Cancelling the enlarged targeting view restores the prior user zoom.
    cancel=d.coords('DEFOLD CAMPAIGN DRONE CANCEL',selection_start);before=len(d.text());d.click(*cancel)
    d.wait('DEFOLD CAMPAIGN DRONE CANCEL PASS stock=3 shots=0 path=0 zoom=',before)
    before=len(d.text());d.click(*badge);option=d.coords('DEFOLD CAMPAIGN DRONE OPTION',before)
    before=len(d.text());d.click(*option)
    preview=d.coords('DEFOLD CAMPAIGN DRONE PREVIEW',before);target=d.coords('DEFOLD CAMPAIGN DRONE TARGET',before)
    if gesture in ['tap','zoom']:
     before=len(d.text());d.click(*target)
    else:
     before=len(d.text());d.drag(preview,target)
    d.wait('DEFOLD CAMPAIGN DRONE FLYING PASS stock=2',before)
    if gesture=='tap':
     active_badge=d.coords('DEFOLD CAMPAIGN INFLIGHT BADGE',before);badge_start=len(d.text());d.click(*active_badge)
     d.wait('DEFOLD CAMPAIGN ACTION drone_open mission=2',badge_start)
    if gesture=='zoom':
     d.click(240,44);d.wait('DEFOLD CAMPAIGN DRONE USER ZOOM DURING FLIGHT PASS',before)
    d.capture('actual-flight',a.output is not None)
    d.wait('DEFOLD CAMPAIGN DRONE IMPACT / NATIVE LIGHTNING PASS stock=2 kills=1 hero_shots=0',before)
    d.capture('native-lightning-impact',a.output is not None)
    d.wait('DEFOLD CAMPAIGN DRONE USER VIEW KEPT PASS'if gesture=='zoom'else'DEFOLD CAMPAIGN DRONE FLIGHT VIEW RESTORED PASS',before)
    assert d.text().count('DEFOLD CAMPAIGN DRONE FLYING PASS')==1,d.text()
    # An extra old release cannot leak out of the consumed tactical gesture.
    d.release(*target);time.sleep(.25)
    assert 'ERROR:'not in d.text(),d.text()
   print('DEFOLD NATIVE DRONE '+gesture.upper()+' / STOCK / FLIGHT / NATIVE LIGHTNING / NO HERO SHOT PASS',flush=True)
 print('DEFOLD NATIVE ATTACK DRONE TAP / DRAG / CANCEL / HUD REJECTION PASS')

if __name__=='__main__':main()
