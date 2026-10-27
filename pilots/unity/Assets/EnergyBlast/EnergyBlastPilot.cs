using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
namespace EnergyBlast {
// Unity import kit. Runtime/Android execution requires the operator's activated Unity Editor.
public sealed class EnergyBlastPilot : MonoBehaviour {
 [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)] static void Boot(){ if(FindObjectOfType<EnergyBlastPilot>()==null)new GameObject("EnergyBlastPilot").AddComponent<EnergyBlastPilot>(); }
 struct Wall { public Rect R; public bool Reflect; public Wall(Rect r,bool b=false){R=r;Reflect=b;} }
 struct Hit { public Vector2 P,N; public float T; public bool Reflect; }
 Mission m; Camera cam; Transform world,hero,guard,secret,goal,gate; MeshFilter cone;
 Vector2 p,g,forward=Vector2.right,aim=new Vector2(.58f,-.81f); Vector2? prediction,trap;
 List<Vector2> route=new List<Vector2>(),trace=new List<Vector2>(); List<Wall> walls=new List<Wall>();
 int missionIndex,patrol,detected; float clock,notice,frozen,retry,traceTime,clueTime,hintCooldown,trapTime;
 bool paused=true,gearMenu,solved,trapUsed,shotPending,shotWin,backgrounded; string mode="move",message="Tippe auf den Boden.",nextVoice;
 AudioSource voice; List<Transform> lights=new List<Transform>();LineRenderer aimLine,traceLine,hintLine;
 [Serializable] sealed class ScoreSave {public List<string> earned=new List<string>();public List<string> clues=new List<string>();public string weapon="pulse";}
 ScoreSave save=new ScoreSave();
 int Stars{get{return save.earned.Sum(k=>PilotData.Rewards.ContainsKey(k)?PilotData.Rewards[k]:0);}}
 int Clues{get{return new[]{"bank","guardian"}.Count(id=>save.earned.Contains("mission:"+id))*2-save.clues.Count;}}
 float Speed{get{return 3+(Stars>=230?Mathf.Min(.5f,(Stars-220)/210f):0);}}
 float Cloak{get{return Stars>=300?Mathf.Min(.35f,(Stars-280)/180f):0;}}
 void Awake(){
  try{var loaded=JsonUtility.FromJson<ScoreSave>(PlayerPrefs.GetString("energyblast.progress",""));if(loaded!=null){save=loaded;save.earned=save.earned.Where(PilotData.Rewards.ContainsKey).Distinct().ToList();save.clues=save.clues.Where(k=>new[]{"bank:1","bank:2","guardian:1","guardian:2"}.Contains(k)).Distinct().ToList();}}catch{}
  cam=new GameObject("Pilot camera").AddComponent<Camera>();cam.orthographic=true;cam.transform.position=new Vector3(0,19,13);cam.transform.LookAt(Vector3.zero);cam.backgroundColor=new Color(.06f,.14f,.20f);cam.clearFlags=CameraClearFlags.SolidColor;
  var light=new GameObject("Sun").AddComponent<Light>();light.type=LightType.Directional;light.intensity=1;light.transform.rotation=Quaternion.Euler(60,-30,0);RenderSettings.ambientLight=new Color(.45f,.5f,.55f);
  voice=gameObject.AddComponent<AudioSource>();voice.playOnAwake=false;voice.volume=.7f;
  Load(0);
 }
 void Save(){PlayerPrefs.SetString("energyblast.progress",JsonUtility.ToJson(save));PlayerPrefs.Save();}
 int Award(string id){if(save.earned.Contains(id))return 0;int before=Stars;save.earned.Add(id);if(before<100&&Stars>=100)save.weapon="prism";Save();return PilotData.Rewards[id];}
 void Say(string id){if(voice.isPlaying){nextVoice=id;return;}var clip=Resources.Load<AudioClip>("EnergyBlast/de/"+id);if(clip!=null){voice.clip=clip;voice.Play();}}
 Material Mat(Color c){var material=new Material(Shader.Find("Standard"));material.color=c;return material;}
 Transform Cube(Vector3 pos,Vector3 size,Color color){var o=GameObject.CreatePrimitive(PrimitiveType.Cube);o.transform.SetParent(world);o.transform.position=pos;o.transform.localScale=size;o.GetComponent<Renderer>().material=Mat(color);Destroy(o.GetComponent<Collider>());return o.transform;}
 Transform Robot(Vector2 at,float scale=1){var prefab=Resources.Load<GameObject>("EnergyBlast/robot");if(prefab==null)throw new InvalidOperationException("Import the shared robot FBX into Assets/Resources/EnergyBlast first.");var o=Instantiate(prefab,world).transform;o.position=new Vector3(at.x,0,at.y);o.localScale=Vector3.one*scale;return o;}
 LineRenderer Line(Color c){var o=new GameObject("Feedback line");o.transform.SetParent(world);var l=o.AddComponent<LineRenderer>();l.material=new Material(Shader.Find("Sprites/Default"));l.startColor=l.endColor=c;l.startWidth=l.endWidth=.055f;l.positionCount=0;return l;}
 void Load(int index){
  if(world!=null)Destroy(world.gameObject);world=new GameObject("Arena").transform;m=PilotData.Missions[index];missionIndex=index;p=m.Spawn;g=m.Patrol.Length>0?m.Patrol[0]:Vector2.zero;clock=notice=retry=frozen=0;patrol=detected=0;prediction=trap=null;route.Clear();trace.Clear();solved=trapUsed=shotPending=false;mode="move";
  Cube(new Vector3(0,-.2f,0),new Vector3(14,.3f,10),new Color(.16f,.3f,.35f));walls.Clear();
  foreach(var r in new[]{new Rect(-7,-5,14,.3f),new Rect(-7,4.7f,14,.3f),new Rect(-7,-5,.3f,10),new Rect(6.7f,-5,.3f,10)})walls.Add(new Wall(r));
  foreach(var r in m.Covers)walls.Add(new Wall(r));foreach(var r in m.Reflectors)walls.Add(new Wall(r,true));
  foreach(var w in walls)Cube(new Vector3(w.R.center.x,.6f,w.R.center.y),new Vector3(w.R.width,1.2f,w.R.height),w.Reflect?new Color(.33f,.9f,.86f):new Color(.26f,.43f,.55f));
  hero=Robot(p);goal=Cube(new Vector3(m.Goal.x,.3f,m.Goal.y),new Vector3(.8f,.6f,.8f),new Color(1,.78f,.36f));secret=Cube(new Vector3(m.Secret.x,.3f,m.Secret.y),new Vector3(.65f,.6f,.5f),new Color(.75f,.5f,.95f));secret.gameObject.SetActive(false);
  lights.Clear();if(m.Patrol.Length>0){guard=Robot(g,1.35f);gate=Cube(new Vector3(m.Gate.center.x,.6f,m.Gate.center.y),new Vector3(m.Gate.width,1.2f,m.Gate.height),new Color(.85f,.6f,.5f));for(int i=0;i<3;i++)lights.Add(Cube(new Vector3(4.2f+i*.6f,1.8f,-1),Vector3.one*.25f,Color.gray));var o=new GameObject("Visible sight cone");o.transform.SetParent(world);cone=o.AddComponent<MeshFilter>();var renderer=o.AddComponent<MeshRenderer>();var mat=Mat(new Color(1,.7f,.25f,.28f));mat.SetFloat("_Mode",3);mat.SetInt("_SrcBlend",5);mat.SetInt("_DstBlend",10);mat.SetInt("_ZWrite",0);mat.EnableKeyword("_ALPHABLEND_ON");mat.renderQueue=3000;renderer.material=mat;}
  aimLine=Line(new Color(.4f,1,.8f));traceLine=Line(new Color(1,.8f,.3f));hintLine=Line(new Color(1,.9f,.6f));message="Tippe auf den Boden.";
 }
 bool Open{get{return clock%8>=5;}}
 List<Wall> ActiveWalls(){var result=new List<Wall>(walls);if(m.Patrol.Length>0&&!Open)result.Add(new Wall(m.Gate));return result;}
 bool Blocked(Vector2 point){if(point.x< -6.5f||point.x>6.5f||point.y< -4.5f||point.y>4.5f)return true;foreach(var w in ActiveWalls()){var r=w.R;r.xMin-=.28f;r.yMin-=.28f;r.xMax+=.28f;r.yMax+=.28f;if(r.Contains(point))return true;}return false;}
 Hit? Ray(Vector2 origin,Vector2 direction,float length,List<Wall> rectangles){Hit? best=null;foreach(var w in rectangles){float[] values={w.R.xMin,w.R.xMax,w.R.yMin,w.R.yMax};Vector2[] normals={Vector2.left,Vector2.right,Vector2.down,Vector2.up};for(int i=0;i<4;i++){int axis=i<2?0:1,other=1-axis;if(Mathf.Abs(direction[axis])<.00001f)continue;float t=(values[i]-origin[axis])/direction[axis];if(t<.001f||t>=length)continue;Vector2 point=origin+direction*t;float lo=other==0?w.R.xMin:w.R.yMin,hi=other==0?w.R.xMax:w.R.yMax;if(point[other]<lo-.0001f||point[other]>hi+.0001f)continue;length=t;best=new Hit{P=point,N=normals[i],T=t,Reflect=w.Reflect};}}return best;}
 List<Vector2> Shot(){var o=p+aim*.35f;var d=aim;var points=new List<Vector2>{o};int bounces=Stars>=100&&save.weapon=="prism"?2:1;float length=28;for(int i=0;i<bounces+2;i++){var h=Ray(o,d,length,ActiveWalls());if(!h.HasValue){points.Add(o+d*length);break;}points.Add(h.Value.P);length-=h.Value.T;if(!h.Value.Reflect||i>=bounces)break;d=Vector2.Reflect(d,h.Value.N);o=h.Value.P+d*.003f;}return points;}
 float SegDistance(Vector2 point,Vector2 a,Vector2 b){var d=b-a;float t=Mathf.Clamp01(Vector2.Dot(point-a,d)/Mathf.Max(.0001f,d.sqrMagnitude));return Vector2.Distance(point,a+d*t);}
 void Navigate(Vector2 target){
  Func<Vector2,Vector2Int> cell=q=>new Vector2Int(Mathf.Clamp(Mathf.RoundToInt((q.x+6.8f)/.4f),0,35),Mathf.Clamp(Mathf.RoundToInt((q.y+4.8f)/.4f),0,25));Func<Vector2Int,Vector2> point=c=>new Vector2(c.x*.4f-6.8f,c.y*.4f-4.8f);Func<Vector2Int,int> key=c=>c.y*36+c.x;
  var start=cell(p);var end=cell(target);if(Blocked(point(end))){float best=10000;for(int x=0;x<36;x++)for(int y=0;y<26;y++){var c=new Vector2Int(x,y);float d=Vector2.Distance(point(c),target);if(!Blocked(point(c))&&d<best){best=d;end=c;}}}
  var q=new List<Vector2Int>{start};var parent=new Dictionary<int,Vector2Int>{{key(start),new Vector2Int(-1,-1)}};bool found=false;
  for(int i=0;i<q.Count;i++){var c=q[i];if(c==end){found=true;break;}for(int dx=-1;dx<=1;dx++)for(int dy=-1;dy<=1;dy++){if(dx==0&&dy==0)continue;var n=c+new Vector2Int(dx,dy);if(n.x<0||n.x>=36||n.y<0||n.y>=26||parent.ContainsKey(key(n))||Blocked(point(n)))continue;if(dx!=0&&dy!=0&&(Blocked(point(c+new Vector2Int(dx,0)))||Blocked(point(c+new Vector2Int(0,dy)))))continue;parent[key(n)]=c;q.Add(n);}}
  route.Clear();if(found){var c=end;while(c.x>=0){route.Insert(0,point(c));c=parent[key(c)];}}else if(m.Patrol.Length>0&&target.y< -1)Navigate(new Vector2(5.1f,0));
 }
 void Touch(Vector2 point){if(retry>0)return;if(mode=="move")Navigate(point);else if(mode=="aim")aim=(point-p).normalized;else if(mode=="predict")prediction=point;else if(mode=="trap"&&!trapUsed&&m.Patrol.Length>0&&Vector2.Distance(p,point)<3.5f&&!Blocked(point)&&!Ray(p,(point-p).normalized,Vector2.Distance(p,point),ActiveWalls()).HasValue){trap=point;trapTime=12;trapUsed=true;mode="move";}}
 void Fire(){if(shotPending)return;if(m.Id=="bank"&&!prediction.HasValue){mode="predict";Say("predict");return;}trace=Shot();traceTime=2.2f;shotPending=true;shotWin=false;if(m.Id=="guardian")for(int i=1;i<trace.Count;i++)if(SegDistance(g,trace[i-1],trace[i])<.7f)frozen=Mathf.Max(frozen,.5f);if(m.Id=="bank")for(int i=1;i<trace.Count-1;i++)if(SegDistance(m.Goal,trace[i],trace[i+1])<(save.earned.Contains("secret:bank")?.7f:.6f)){shotWin=true;trace=trace.Take(i+2).ToList();trace[i+1]=m.Goal;break;}}
 int ClueLevel{get{return save.clues.Count(x=>x.StartsWith(m.Id+":"));}}
 void Hint(){if(hintCooldown>0)return;hintCooldown=1.2f;if(ClueLevel<2){if(Clues<=0){Say("hints_empty");return;}save.clues.Add(m.Id+":"+(ClueLevel+1));Save();}clueTime=8;Say("hint_"+m.Id);}
 void Finish(bool skill){if(solved)return;solved=true;route.Clear();int n=Award("mission:"+m.Id);if(skill)n+=Award("skill:"+m.Id);message="Geschafft! + "+n+" ★";paused=true;Say("success");}
 void Draw(LineRenderer l,List<Vector2> points){l.positionCount=points.Count;for(int i=0;i<points.Count;i++)l.SetPosition(i,new Vector3(points[i].x,.1f,points[i].y));}
 void Animate(Transform robot,bool moving){float wave=Mathf.Sin(clock*11)*(moving?.5f:.04f);foreach(var t in robot.GetComponentsInChildren<Transform>())if(t.name=="Leg_L"||t.name=="Arm_R")t.localRotation=Quaternion.Euler(wave*57,0,0);else if(t.name=="Leg_R"||t.name=="Arm_L")t.localRotation=Quaternion.Euler(-wave*57,0,0);}
 void Update(){
  cam.orthographicSize=Mathf.Max(5.75f,7.9f/cam.aspect);if(!voice.isPlaying&&nextVoice!=null){var id=nextVoice;nextVoice=null;Say(id);}if(paused||backgrounded)return;float dt=Mathf.Min(Time.deltaTime,.05f);clock+=dt;hintCooldown-=dt;clueTime-=dt;traceTime-=dt;
  if(shotPending&&traceTime<1.45f){shotPending=false;if(shotWin)Finish(prediction.HasValue&&Vector2.Distance(prediction.Value,m.Goal)<1);else if(m.Id=="bank")Say("again");}
  if(retry>0){retry-=dt;if(retry<=0){p=m.Spawn;notice=0;trapUsed=false;trap=null;}}else if(route.Count>0){var target=route[0];var next=Vector2.MoveTowards(p,target,Speed*dt);if(!Blocked(next)){var d=next-p;if(d.sqrMagnitude>.0001f)hero.rotation=Quaternion.Euler(0,Mathf.Atan2(d.x,d.y)*Mathf.Rad2Deg,0);p=next;}else route.Clear();if(route.Count>0&&Vector2.Distance(p,route[0])<.04f)route.RemoveAt(0);}
  hero.position=new Vector3(p.x,0,p.y);Animate(hero,route.Count>0);if(m.Patrol.Length>0)TickGuardian(dt);
  float distance=Vector2.Distance(p,m.Secret);bool visible=!save.earned.Contains("secret:"+m.Id)&&distance<2&&!Ray(p,(m.Secret-p).normalized,distance-.05f,walls).HasValue;secret.gameObject.SetActive(visible);if(visible&&distance<.7f){Award("secret:"+m.Id);Say("found");secret.gameObject.SetActive(false);}
  Draw(aimLine,mode=="aim"||mode=="predict"?Shot().Take(2).ToList():new List<Vector2>());Draw(traceLine,traceTime>0?trace:new List<Vector2>());Draw(hintLine,clueTime>0?new List<Vector2>{p,ClueLevel>=2?m.Secret:m.Landmark}:new List<Vector2>());
  if(Input.touchCount>0){var t=Input.GetTouch(0);if(t.phase==TouchPhase.Began)HandleScreen(t.position);}else if(Input.GetMouseButtonDown(0))HandleScreen(Input.mousePosition);
 }
 void HandleScreen(Vector2 screen){float y=Screen.height-screen.y;if(y<100f*Screen.width/720||y>Screen.height-220f*Screen.width/720)return;var ray=cam.ScreenPointToRay(screen);if(new Plane(Vector3.up,Vector3.zero).Raycast(ray,out float d)){var h=ray.GetPoint(d);Touch(new Vector2(Mathf.Clamp(h.x,-6.4f,6.4f),Mathf.Clamp(h.z,-4.3f,4.3f)));}}
 void TickGuardian(float dt){
  frozen=Mathf.Max(0,frozen-dt);if(frozen<=0){var t=m.Patrol[(patrol+1)%m.Patrol.Length];forward=(t-g).normalized;g=Vector2.MoveTowards(g,t,1.6f*dt);if(Vector2.Distance(g,t)<.06f)patrol=(patrol+1)%m.Patrol.Length;}guard.position=new Vector3(g.x,0,g.y);guard.rotation=Quaternion.Euler(0,Mathf.Atan2(forward.x,forward.y)*Mathf.Rad2Deg,0);Animate(guard,frozen<=0);
  if(trap.HasValue&&Vector2.Distance(trap.Value,g)<1.05f){frozen=3.5f;trap=null;}if(trap.HasValue){trapTime-=dt;if(trapTime<=0)trap=null;}float range=5.5f*(1-Cloak)*(save.earned.Contains("secret:guardian")?.9f:1);var delta=p-g;bool seen=frozen<=0&&delta.magnitude<range&&Vector2.Dot(delta.normalized,forward)>Mathf.Cos(35*Mathf.Deg2Rad)&&!Ray(g,delta.normalized,delta.magnitude-.02f,walls).HasValue;notice=Mathf.Max(0,notice+(seen?dt:-dt*2));if(notice>=(Stars>=160?1.4f:1)&&retry<=0){detected++;retry=.9f;route.Clear();Say("seen");}
  var vertices=new List<Vector3>();var triangles=new List<int>();float angle=Mathf.Atan2(forward.y,forward.x);for(int i=0;i<40;i++){Vector2[] edges=new Vector2[2];for(int j=0;j<2;j++){float a=angle+(-35+(i+j)*70f/40)*Mathf.Deg2Rad;var d=new Vector2(Mathf.Cos(a),Mathf.Sin(a));var h=Ray(g,d,range,walls);edges[j]=h.HasValue?h.Value.P:g+d*range;}int n=vertices.Count;vertices.Add(new Vector3(g.x,.03f,g.y));vertices.Add(new Vector3(edges[1].x,.03f,edges[1].y));vertices.Add(new Vector3(edges[0].x,.03f,edges[0].y));triangles.AddRange(new[]{n,n+1,n+2,n,n+2,n+1});}if(cone.sharedMesh!=null)Destroy(cone.sharedMesh);var mesh=new Mesh();mesh.SetVertices(vertices);mesh.SetTriangles(triangles,0);mesh.RecalculateNormals();cone.sharedMesh=mesh;
  gate.localScale=new Vector3(m.Gate.width,Open?.12f:1.2f,m.Gate.height);for(int i=0;i<3;i++)lights[i].GetComponent<Renderer>().material.color=clock%8>=3+i?Color.green:Color.gray;if(!solved&&p.y< -1.4f&&Vector2.Distance(p,m.Goal)<.8f)Finish(detected==0);
 }
 void OnApplicationPause(bool pause){backgrounded=pause;if(pause)voice.Pause();else voice.UnPause();}
 void OnGUI(){
  float scale=Screen.width/720f,height=Screen.height/scale;GUI.matrix=Matrix4x4.Scale(Vector3.one*scale);GUI.skin.button.fontSize=22;GUI.skin.label.fontSize=26;GUI.color=Color.white;
  GUI.Label(new Rect(20,20,300,60),"★ "+Stars+"     ? "+Clues);if(GUI.Button(new Rect(470,12,110,68),"Karten")){paused=true;gearMenu=false;}if(GUI.Button(new Rect(590,12,110,68),"Ton"))voice.mute=!voice.mute;
  GUI.Label(new Rect(30,height-245,660,45),message);var ids=new[]{"move","aim","predict","fire","trap"};var titles=new[]{"Laufen","Zielen","Tipp","Schuss","Fangfeld"};for(int i=0;i<5;i++)if(GUI.Button(new Rect(12+i*140,height-190,134,84),titles[i])){if(ids[i]=="fire")Fire();else{mode=ids[i];route.Clear();Say(mode);}}
  if(GUI.Button(new Rect(12,height-94,222,76),"? Hinweis"))Hint();if(GUI.Button(new Rect(246,height-94,222,76),"Erklären"))Say("intro_"+m.Id);if(GUI.Button(new Rect(480,height-94,222,76),"Ausrüstung")){paused=true;gearMenu=true;}
  if(paused){var box=new Rect(70,height/2-230,580,470);GUI.Box(box,gearMenu?"Ausrüstung":"EnergyBlast");if(gearMenu){GUI.Label(new Rect(95,box.y+45,530,50),"100 ★ Prisma · 160 ★ Rüstung");GUI.Label(new Rect(95,box.y+100,530,50),"230 ★ Tempo · 300 ★ Tarnung");if(Stars>=100&&GUI.Button(new Rect(100,box.y+170,520,70),"Prisma / Impuls wechseln")){save.weapon=save.weapon=="prism"?"pulse":"prism";Save();}}else for(int i=0;i<2;i++){int index=i;if(GUI.Button(new Rect(100,box.y+55+i*110,520,90),PilotData.Missions[i].Title)){Load(index);paused=false;voice.Stop();Say("intro_"+m.Id);}}if(GUI.Button(new Rect(100,box.y+350,520,80),"Weiter")){paused=false;gearMenu=false;}}
 }
}
}
