
#define DEBUG_NETWORK

using UnityEngine;

using System;
using System.Net;
using System.Net.Sockets;
using System.Threading;

/// <summary>
/// Class to manage DMX data for the cube
/// </summary>
public class DMX_Controller : MonoBehaviour
{
    private LedsManager leds_manager;


    // receiving Thread
    Thread receiveThread;

    // Udpclient object
    UdpClient client;

    public int port = 6454;

    private bool running;

 

    // start from unity3d
    /// <summary>
    /// function start form unity3d
    /// This function start the thread
    /// </summary>
    public void Start()
    {
        leds_manager = this.GetComponent<LedsManager>();


        receiveThread = new Thread(new ThreadStart(ReceiveDMX));
        receiveThread.IsBackground = true;
        receiveThread.Start();
    }
    
    // receive thread
    /// <summary>
    /// Function that manage DMX paquet for the cube
    /// </summary>
    private void ReceiveDMX()
    {

        IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, 0);
        client = new UdpClient(port);
        running = true;


        while (running)
        {
            try
            {
                byte[] data = client.Receive(ref anyIP);
      
                if (data.Length >= 14) {

                    // Ar-Net header
                    byte[] artnet_bytes = new byte[7];
                    System.Array.Copy(data, 0, artnet_bytes, 0, 7);
                    string artnet_str = System.Text.Encoding.Default.GetString(artnet_bytes);
                    uint opcode = (uint)data[9] << 8;
                    opcode |= data[8];

                    uint version = (uint)data[10] << 8;
                    version |= data[11];


                   
                    // Check if the packet is form Art-Net
                    if (artnet_str == "Art-Net" && opcode == 0x5000 && version == 14)
                    {

                        //string packet_log = "";
                        //for (int i = 0; i < data.Length; i++)                        
                        //    packet_log += String.Format("{00:X}", data[i]) + " ";
                        //Debug.Log("Packet = " + packet_log);


                        //TODO check the protocol version and others fields ??

                        // Universe
                        byte mask = 0x7f;
                        data[15] &= mask;

                        uint universe = data[15];
                        universe = universe << 8;
                        universe |= data[14];

                        // Length of data
                        uint HLength = data[16];
                        uint LLength = data[17];
                        HLength = HLength << 8;
                        HLength |= LLength;

                        // Values of leds
                        byte[] values = new byte[HLength];
                        System.Array.Copy(data, 18, values, 0, HLength);

                        // Blink leds
                        leds_manager.blinkLeds(universe, values);

                        //Debug.Log("universe = " + universe);
                        //string log = "";
                        //for (int i = 0; i < HLength; i++)
                        //    log += String.Format("{00:X}", values[i]) + " ";
                        //Debug.Log("buffer = " + log);
                    }
                }
            }
            catch (Exception err)
            {
                Debug.LogError(err.ToString());
            }
        }
    }

    /// <summary>
    /// Function to close connection and kill thread when application is close
    /// </summary>
    private void OnDisable()
    {
        client.Close();
        running = false;
    }
   
}