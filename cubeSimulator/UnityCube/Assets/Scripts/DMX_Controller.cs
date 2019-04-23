
#define DEBUG_NETWORK

using UnityEngine;

using System;
using System.Net;
using System.Net.Sockets;
using System.Threading;

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
    public void Start()
    {
        leds_manager = this.GetComponent<LedsManager>();

        receiveThread = new Thread(new ThreadStart(ReceiveDMX));
        receiveThread.IsBackground = true;
        receiveThread.Start();
    }
    
    // receive thread
    private void ReceiveDMX()
    {
        client = new UdpClient(port);

        running = true;

        while (running)
        {
            try
            {
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, 0);
                byte[] data = client.Receive(ref anyIP);

                if (data.Length >= 20) {

                    // Ar-Net header
                    byte[] artnet_bytes = new byte[8];
                    System.Array.Copy(data, 0, artnet_bytes, 0, 8);
                    string artnet_str = System.Text.Encoding.Default.GetString(artnet_bytes);
                   
                    // Check if the packet is form Art-Net
                    if (artnet_str != "Art-Net")
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

    private void OnDisable()
    {
        client.Close();
        running = false;
    }
   
}