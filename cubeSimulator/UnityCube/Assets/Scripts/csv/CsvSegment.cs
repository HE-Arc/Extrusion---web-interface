using System;

[Serializable]
public class CsvSegment
{
    public int axis_x { get; set; }
    public int axis_y { get; set; }
    public int axis_z { get; set; }
    public int universe1 { get; set; }
    public int universe2 { get; set; }
    public int channelStart1 { get; set; }
    public int channelEnd1 { get; set; }
    public int channelStart2 { get; set; }
    public int channelEnd2 { get; set; }
    public bool reverse { get; set; }
}

