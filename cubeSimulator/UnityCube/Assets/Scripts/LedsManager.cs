using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using UnityEngine;

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

public class LedsManager : MonoBehaviour {

    // Number of leds by segment
    public int segmentLength = 0;

    // Distance between each leds on a segment
    public float scale = 0f;

    // 2D sprite of the Led wich will instantiate
    public Transform Led;

    // Define an array of leds segments (see documentation).
    private Dictionary<string, Transform> segments_dic = new Dictionary<string, Transform>();

    // Number max of universe supported 
    private const int nb_universe = 500;

    // Table to store spriterenderer components (of each leds)
    private Dictionary<string, SpriteRenderer> leds_by_universe = new Dictionary<string, SpriteRenderer>();

    // Request recivied by the DMX controller
    public List<DMX_Leds> requests = new List<DMX_Leds>();

    private const int DMX_UNIVERSE_SIZE = 512;
    private const int DMX_LED_SIZE = 3;
    private const float LED_OFF_VALUE = 0f;

    // Use this for initialization
    void Start ()
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
            if (name.Length < 13)
                continue;

            // Check the format of the name
            if (name.Substring(0, 8) != "Segment-")
                continue;

            // Coordinates
            int x, y;

            // Try to decode the name of the gameObject
            if (int.TryParse(name.Substring(8, 2), out x) && int.TryParse(name.Substring(11, 2), out y))
            {
                // Store the segment
                segments_dic.Add(x + "-" + y, segment_object);

                // Display the value in the editor
                DebugSegment debug = segment_object.GetComponent<DebugSegment>();
                debug.setCoordinates(x, y, false);
            }            
        }

        // Read json file to get the adress of each led (univers + channel).
        // The adress were stored for each segment.
        TextAsset cube_asset = Resources.Load<TextAsset>("json/Cube");
        JsonSegment[] json_segments = JsonHelper.FromJson<JsonSegment>(cube_asset.text);

        // For all segments stored in the json
        // Find the corresponding unity object in the scene
        // Instantiate the leds of the segment
        foreach (JsonSegment json in json_segments)
        {
            // Find the segment in the scene
            Transform segment;
            bool segment_found = segments_dic.TryGetValue(json.axis_x + "-" + json.axis_y, out segment);

            // If the object exist in Unity scene
            if(segment_found)
            {
                int address = json.channel;   // Start address in the universe
                int universe = json.universe; // Universe

                // For each leds set the channel and the universe
                for (int i = 0; i < segmentLength; i++)
                {
                    // Instantiate a led at the right position in the segment parent
                    Transform led_object = Instantiate(Led, segment.position + segment.right * i * scale, segment.rotation);
                    led_object.SetParent(segment);

                    //Set the name (key in dictionnary)
                    led_object.name = "Led-" + universe + "-" + address;

                    // Set opacity of the sprite to null
                    SpriteRenderer sprite_renderer = led_object.GetComponent<SpriteRenderer>();
                    sprite_renderer.color = new Color(1f, 1f, 1f, LED_OFF_VALUE);

                    // Store the led in the table
                    leds_by_universe.Add(led_object.name, sprite_renderer);

                    // Display the value in the editor
                    DebugLed debug = led_object.GetComponent<DebugLed>();
                    debug.setConfigLed(universe, address);

                    // Set the next address : each DMX led take 3 bytes
                    address += 3;

                    // Take the next universe if the first universe is full
                    if (address > DMX_UNIVERSE_SIZE - DMX_LED_SIZE) {
                        universe++;
                        address = 0;
                    }
                }
            }
        }
    }

    void Update()
    {   
        if (requests.Count > 0)
        {
            // For each leds in the universe set the opacity of the sprite
            for (int i = 0; i < 512; i++)
            {
                SpriteRenderer blinker;

                // If the led exist
                if (leds_by_universe.TryGetValue("Led-" + requests[0].universe + "-" + i, out blinker))
                {
                    // Set the opacity of the sprite
                    blinker.color = new Color(1f, 1f, 1f, requests[0].buffer[i] / 255.0f);
                }
            }

            // Remove the request
            requests.RemoveAt(0);
        }
    }

    // Call by the DMX controller
    public void blinkLeds(uint universe, byte[] values)
    {
        requests.Add(new DMX_Leds((int)universe, values));
    }
}
