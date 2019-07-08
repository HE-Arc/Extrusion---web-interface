using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DebugSegment : MonoBehaviour
{
    public int axis_x = -1;
    public int axis_y = -1;
    public int axis_z = -1;
    public bool revertAdress = false;


    public void setCoordinates(int x, int y, int z, bool revertAdress)
    {
        axis_x = x;
        axis_y = y;
        axis_z = z;
        this.revertAdress = revertAdress;
    }
}
