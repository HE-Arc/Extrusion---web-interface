using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DebugLed : MonoBehaviour {

    public int universe = -1;
    public int channel = -1;

    public void setConfigLed(int universe, int channel)
    {
        this.universe = universe;
        this.channel = channel;
    }
}
