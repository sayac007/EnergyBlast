#if UNITY_EDITOR
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
namespace EnergyBlast {
 public static class BuildPilot {
  [MenuItem("EnergyBlast/Create pilot scene")]
  public static void CreateScene(){var scene=EditorSceneManager.NewScene(NewSceneSetup.EmptyScene,NewSceneMode.Single);new GameObject("EnergyBlastPilot").AddComponent<EnergyBlastPilot>();EditorSceneManager.SaveScene(scene,"Assets/EnergyBlastPilot.unity");}
  [MenuItem("EnergyBlast/Build Android debug APK")]
  public static void Android(){CreateScene();PlayerSettings.companyName="EnergyBlast";PlayerSettings.productName="EnergyBlast Unity Pilot";PlayerSettings.SetApplicationIdentifier(BuildTargetGroup.Android,"org.example.energyblast.unity");PlayerSettings.bundleVersion="0.1.0";PlayerSettings.Android.bundleVersionCode=1;PlayerSettings.Android.minSdkVersion=(AndroidSdkVersions)24;PlayerSettings.Android.targetSdkVersion=(AndroidSdkVersions)36;PlayerSettings.Android.allowBackup=false;EditorUserBuildSettings.buildAppBundle=false;System.IO.Directory.CreateDirectory("Build");BuildPipeline.BuildPlayer(new[]{"Assets/EnergyBlastPilot.unity"},"Build/energyblast-unity-debug.apk",BuildTarget.Android,BuildOptions.Development);}
 }
}
#endif
