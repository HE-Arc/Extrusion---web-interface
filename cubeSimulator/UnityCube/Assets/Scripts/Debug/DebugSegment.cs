using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// Data class to stor Segement model information to show in unity editor
/// </summary>
public class DebugSegment : MonoBehaviour
{
    public int axis_x = -1;
    public int axis_y = -1;
    public int axis_z = -1;
    public bool revertAdress = false;

    /// <summary>
    /// Function to set segement model segement datas
    /// </summary>
    /// <param name="x">x coordinate of segement</param>
    /// <param name="y">y coordinate of segement</param>
    /// <param name="z">z coordinate of segement</param>
    /// <param name="revertAdress">Boolean if segement follow xyz coordinate system</param>
    public void setCoordinates(int x, int y, int z, bool revertAdress)
    {
        axis_x = x;
        axis_y = y;
        axis_z = z;
        this.revertAdress = revertAdress;
    }
}
