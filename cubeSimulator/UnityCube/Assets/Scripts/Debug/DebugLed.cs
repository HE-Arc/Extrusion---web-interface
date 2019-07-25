using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// Data Class to store Led model information to show to unity editor
/// </summary>
public class DebugLed : MonoBehaviour {

    public int universe = -1;
    public int channel = -1;

    /// <summary>
    /// Function to set led model datas
    /// </summary>
    /// <param name="universe">universe of led</param>
    /// <param name="channel">start chanel of led</param>
    public void setConfigLed(int universe, int channel)
    {
        this.universe = universe;
        this.channel = channel;
    }
}
