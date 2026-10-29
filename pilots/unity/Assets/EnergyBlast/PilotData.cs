using UnityEngine;
using System.Collections.Generic;
namespace EnergyBlast {
public static class PilotData {
public static Mission[] Missions = new Mission[] {
new Mission { Id="bank", Title="Bandenschalter", Spawn=new Vector2(-4.0f,3.2f), Goal=new Vector2(4.5f,0.0f), Covers=new Rect[] {new Rect(-0.7f,-0.6f,1.4f,3.6f),new Rect(-5.3f,-1.8f,1.5f,1.0f)}, Reflectors=new Rect[] {new Rect(-6.7f,-4.6f,13.4f,0.25f),new Rect(6.45f,-4.1f,0.25f,8.2f)}, Secret=new Vector2(-4.5f,-2.5f), Landmark=new Vector2(-4.5f,-1.3f), Gate=new Rect(), Patrol=new Vector2[] {}},
new Mission { Id="guardian", Title="Wächter und Energietor", Spawn=new Vector2(-5.5f,3.5f), Goal=new Vector2(5.2f,-3.5f), Covers=new Rect[] {new Rect(-3.0f,-1.5f,2.0f,3.0f),new Rect(0.8f,0.4f,1.6f,1.8f),new Rect(3.5f,-4.7f,0.25f,3.7f)}, Reflectors=new Rect[] {}, Secret=new Vector2(-1.8f,-2.4f), Landmark=new Vector2(-2.0f,-0.4f), Gate=new Rect(3.75f,-1.15f,2.95f,0.3f), Patrol=new Vector2[] {new Vector2(-4.0f,-2.6f),new Vector2(2.95f,-2.6f),new Vector2(2.95f,2.9f),new Vector2(-4.0f,2.9f)}},
};
public static Dictionary<string,int> Rewards = new Dictionary<string,int> {
{"mission:bank",75},
{"skill:bank",25},
{"secret:bank",50},
{"mission:guardian",100},
{"skill:guardian",25},
{"secret:guardian",50},
};
}
public class Mission {public string Id,Title; public Vector2 Spawn,Goal,Secret,Landmark; public Rect[] Covers,Reflectors; public Rect Gate; public Vector2[] Patrol;}
}