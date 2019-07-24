using System;

/// <summary>
/// Data Class to store csv segement informations
/// </summary>
[Serializable]
public class CsvSegment
{
    public int AxisX { get; set; }
    public int AxisY { get; set; }
    public int AxisZ { get; set; }
    public int Universe1 { get; set; }
    public int Universe2 { get; set; }
    public int ChannelStart1 { get; set; }
    public int ChannelEnd1 { get; set; }
    public int ChannelStart2 { get; set; }
    public int ChannelEnd2 { get; set; }
    public bool Reverse { get; set; }
}

