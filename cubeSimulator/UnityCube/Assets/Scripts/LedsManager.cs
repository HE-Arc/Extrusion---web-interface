﻿using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Threading;
using UnityEngine;

/// <summary>
/// Data Class to store information recieve in DMX network paquet
/// </summary>
public class DMX_Leds
{
    public DMX_Leds(int universe, byte[] buffer)
    {
        this.universe = universe;
        this.buffer = buffer;
    }

    public int universe;
    public byte[] buffer;
}

/// <summary>
/// Class to manage led on the cube
/// </summary>
public class LedsManager : MonoBehaviour
{

    // Number of leds by segment
    public int segmentLength = 0;

    // Distance between each leds on a segment
    public float scale = 0f;

    // 2D sprite of the Led wich will instantiate
    public Transform Led;

    // Define an array of leds segments (see documentation).
    private Dictionary<string, Transform> segments_dic = new Dictionary<string, Transform>();

    // Number max of universe supported 
    private const int nb_universe = 50;

    // Table to store spriterenderer components (of each leds)
    private Dictionary<string, List<SpriteRenderer>> leds_by_universe = new Dictionary<string, List<SpriteRenderer>>();

    // Request recivied by the DMX controller
    public Queue<DMX_Leds> requests = new Queue<DMX_Leds>();

    private const int DMX_UNIVERSE_SIZE = 512;
    private const int DMX_LED_SIZE = 3;
    private const float LED_OFF_VALUE = 0f;


    // Use this for initialization
    /// <summary>
    /// function start form unity3d
    /// Create all the led on the specific part of the cube
    /// </summary>
    void Start()
    {
        // Get all gameobjects with the tag "Segment".
        // GameObject[] segments_objects = GameObject.FindGameObjectsWithTag("Segment");
        Transform[] segments_objects = GetComponentsInChildren<Transform>();

        // Order gameobjects segments in 2 dimensionnal array (see documentation).
        foreach (Transform segment_object in segments_objects)
        {
            // The name of gameObject is used to set the coordinate.
            // => Segment-XX-YY
            string name = segment_object.gameObject.name;

            // Check the format of the name
            if (name.Length < 17)
                continue;

            // Check the format of the name
            if (name.Substring(0, 8) != "Segment-")
                continue;

            // Coordinates
            int x, y, z, reversed;


            // Try to decode the name of the gameObject
            if (int.TryParse(name.Substring(8, 2), out x) && int.TryParse(name.Substring(11, 2), out y)
                && int.TryParse(name.Substring(14, 2), out z) && int.TryParse(name.Substring(17, 1), out reversed))
            {
                // Store the segment
                segments_dic.Add(x + "-" + y + "-" + z, segment_object);

                // Display the value in the editor
                DebugSegment debug = segment_object.GetComponent<DebugSegment>();
                debug.setCoordinates(x, y, z, System.Convert.ToBoolean(reversed));
            }
        }

        // Read csv file to get the address of each led (univers + channel).
        // The adress were stored for each segment.
        //TextAsset cube_asset = Resources.Load<TextAsset>("xyz/xyz");
        //JsonSegment[] json_segments = JsonHelper.FromJson<JsonSegment>(cube_asset.text);

        TextAsset cube_asset = Resources.Load<TextAsset>("xyz/xyz");
        List<CsvSegment> csv_segments = CsvHelper.FromCsv(cube_asset.text);


        // For all segments stored in the json
        // Find the corresponding unity object in the scene
        // Instantiate the leds of the segment

        foreach (CsvSegment csv in csv_segments)
        {

            // Find the segment in the scene
            Transform segment;
            bool segment_found = segments_dic.TryGetValue(csv.AxisX + "-" + csv.AxisY + "-" + csv.AxisZ, out segment);
            // If the object exist in Unity scene
            if (segment_found && csv.Universe1 != -1)
            {
                bool reverse = isReversed(csv.Reverse, segment.GetComponent<DebugSegment>().revertAdress);
                if (csv.Universe2 == -1)
                {
                    addLedNormalSegement(segment, csv, reverse);
                }
                else
                {
                    addSeparatedSegment(segment, csv, reverse);
                }
            }
        }
    }

    /// <summary>
    /// function to create led when ledstrip addresses is on 2 universe
    /// </summary>
    /// <param name="segment">unity model on cube</param>
    /// <param name="csv"> segement address information</param>
    /// <param name="reverse">the direction</param>
    private void addSeparatedSegment(Transform segment, CsvSegment csv, bool reverse)
    {

        int position = 0;
        if (reverse)
        {
            int universe = csv.Universe2;
            for (int i = csv.ChannelEnd2 - 2; i >= csv.ChannelStart2; i = i - 3)
            {
                addToScene(segment, universe, i, position);
                position++;
            }

            universe = csv.Universe1;
            for (int i = csv.ChannelEnd1 - 2; i >= csv.ChannelStart1; i = i - 3)
            {
                addToScene(segment, universe, i, position);
                position++;
            }
        }
        else
        {
            int universe = csv.Universe1;
            for (int i = csv.ChannelStart1; i <= csv.ChannelEnd1 - 2; i = i + 3)
            {
                addToScene(segment, universe, i, position);
                position++;
            }

            universe = csv.Universe2;
            for (int i = csv.ChannelStart2; i <= csv.ChannelEnd2 - 2; i = i + 3)
            {
                addToScene(segment, universe, i, position);
                position++;
            }
        }

    }
    /// <summary>
    /// function to create led when ledstrip addresses is on 1 universe
    /// </summary>
    /// <param name="segment">unity model on cube</param>
    /// <param name="csv"> segement address information</param>
    /// <param name="reverse">the direction</param>
    private void addLedNormalSegement(Transform segment, CsvSegment csv, bool reverse)
    {
        int position = 0;
        if (reverse)
        {
            int universe = csv.Universe1;
            for (int i = csv.ChannelEnd1 - 2; i >= csv.ChannelStart1; i = i - 3)
            {
                addToScene(segment, universe, i, position);
                position++;
            }
        }
        else
        {
            int universe = csv.Universe1;
            for (int i = csv.ChannelStart1; i <= csv.ChannelEnd1 - 2; i = i + 3)
            {
                addToScene(segment, universe, i, position);
                position++;
            }
        }
        // For each leds set the channel and the universe

    }

    /// <summary>
    /// Add leds on the segement
    /// </summary>
    /// <param name="segment">segement to add leds</param>
    /// <param name="universe">universe of the segement</param>
    /// <param name="address">start adress of led</param>
    /// <param name="position">position of the led</param>
    void addToScene(Transform segment, int universe, int address, int position)
    {
        // Instantiate a led at the right position in the segment parent
        Transform led_object = Instantiate(Led, segment.position + segment.right * position * scale, segment.rotation);
        led_object.SetParent(segment);

        //Set the name (key in dictionnary)
        led_object.name = "Led-" + universe + "-" + address;
        // Set opacity of the sprite to null
        SpriteRenderer sprite_renderer = led_object.GetComponent<SpriteRenderer>();
        sprite_renderer.color = new Color(1f, 1f, 1f, LED_OFF_VALUE);
        List<SpriteRenderer> list_led;
        if (leds_by_universe.TryGetValue(led_object.name, out list_led))
        {
            list_led.Add(sprite_renderer);
        }
        else
        {
            // Store the led in the table
            leds_by_universe.Add(led_object.name, new List<SpriteRenderer> { sprite_renderer });
        }

        // Display the value in the editor
        DebugLed debug = led_object.GetComponent<DebugLed>();
        debug.setConfigLed(universe, address);
    }


    /// <summary>
    /// Function that display the scene with a fps
    /// This function use DMX_Led data in the queue to update the illuminsation of the led in scene
    /// </summary>
    void Update()
    {
        int size;

        size = requests.Count;

        Debug.Log(size);
        if (size > 45)
        {
            for (var j = 0; j < 45; j++)
            {
                var data = requests.Dequeue();
                // For each leds in the universe set the opacity of the sprite
                for (int i = 0; i < 512; i++)
                {

                    List<SpriteRenderer> blinkers;

                    // If the led exist
                    if (leds_by_universe.TryGetValue("Led-" + data.universe + "-" + i, out blinkers))
                    {
                        // Set the opacity of the sprite
                        foreach (var sprite in blinkers)
                        {
                            sprite.color = new Color(1f, 1f, 1f, data.buffer[i] / 15.0f);
                        }
                    }
                }
            }
        }
    }

    /// <summary>
    /// function to put DMX data in the queue
    /// </summary>
    /// <param name="universe">DMX unviverse</param>
    /// <param name="values">Byte array of DMX data</param>
    public void blinkLeds(uint universe, byte[] values)
    {
           requests.Enqueue(new DMX_Leds((int)universe, values));
    }
    /// <summary>
    /// Functio to know if the led in segement must follow the direction or revers it
    /// </summary>
    /// <param name="cubeReverseXyzSystem">led addresses on cube follow xyz coordinate system</param>
    /// <param name="unityReverseXyzSystem">Segement in unity follow xyz coordinate system</param>
    /// <returns></returns>
    private static bool isReversed(bool cubeReverseXyzSystem, bool unityReverseXyzSystem)
    {
        return cubeReverseXyzSystem ^ unityReverseXyzSystem;
    }
}
