﻿using System;
using UnityEngine;
using System.Collections;
using System.Collections.Generic;

/// <summary>
/// Class to convert csv file into CsvSegement
/// </summary>
[Serializable]
public static class CsvHelper
{
    private static char lineSeperator = '\n';
    private static char fieldSeperator = ';';

    /// <summary>
    /// Function to convert csv file into CsvSegement list
    /// </summary>
    /// <param name="csv">csv string</param>
    /// <returns>list of CsvSegement that was in the csv string</returns>
    public static List<CsvSegment> FromCsv(string csv)
    {
        List<CsvSegment> listSegement = new List<CsvSegment>();
        string[] lines = csv.Split(lineSeperator);
        foreach (string line in lines)
        {
            bool reverse;
            string[] datas = line.Split(fieldSeperator);
            var addresses = Parseaddress(datas[4]);
            var universe = ParseUni(datas[3]);
            try
            {
                reverse = (Convert.ToInt32(datas[5]) == 0);
            }
            catch (IndexOutOfRangeException e)
            {
                reverse = false;
            }

            listSegement.Add(new CsvSegment
            {
                AxisX = Convert.ToInt32(datas[0]),
                AxisY = Convert.ToInt32(datas[1]),
                AxisZ = Convert.ToInt32(datas[2]),
                Universe1 = universe[0],
                Universe2 = universe[1],
                ChannelStart1 = addresses[0],
                ChannelEnd1 = addresses[1],
                ChannelStart2 = addresses[2],
                ChannelEnd2 = addresses[3],
                Reverse = reverse,
            });
            }
            return listSegement;
        }

        /// <summary>
        /// Function to find 1 or 2 univers 
        /// </summary>
        /// <param name="data">string where there are universe</param>
        /// <returns>list of unvivers that were in the string</returns>
        public static int[] ParseUni(string data)
        {
            int[] universe = new int[2];

            if (int.TryParse(data, out universe[0]))
            {
                universe[1] = -1;
                return universe;
            }
            else
            {

                var universe_data = data.Split('/');
                if (int.TryParse(universe_data[0], out universe[0]) && int.TryParse(universe_data[1], out universe[1]))
                {
                    return universe;
                }
            }
            universe[0] = -1;
            universe[1] = -1;
            return universe;
        }

        /// <summary>
        /// Function to find addresses 
        /// </summary>
        /// <param name="data">string where there are addresses</param>
        /// <returns>list of addresses that were in the string</returns>
        public static int[] Parseaddress(string data)
        {
            int[] ArrayAddress = new int[4];
            var addresses = data.Split('/');
            if (addresses.Length == 2)
            {

                var address1 = addresses[0].Split('-');
                var address2 = addresses[1].Split('-');
                if (int.TryParse(address1[0], out ArrayAddress[0]) && int.TryParse(address1[1], out ArrayAddress[1])
                    && int.TryParse(address2[0], out ArrayAddress[2]) && int.TryParse(address2[1], out ArrayAddress[3]))
                {

                    return ArrayAddress;
                }

            }
            else
            {
                var address = addresses[0].Split('-');
                if (int.TryParse(address[0], out ArrayAddress[0]) && int.TryParse(address[1], out ArrayAddress[1]))
                {
                    ArrayAddress[2] = -1;
                    ArrayAddress[3] = -1;
                    return ArrayAddress;
                }

            }

            ArrayAddress[0] = -1;
            ArrayAddress[1] = -1;
            ArrayAddress[2] = -1;
            ArrayAddress[3] = -1;
            return ArrayAddress;


        }



    }

