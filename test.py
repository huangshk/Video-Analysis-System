#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author       : Shuokang Huang
# @Organization : Peking University
# @Time         : 2020/10/25 23:00
#
#
#
import os, json, requests
#
#
#
def auto_request(var_path, var_base_url):
    #
    ##  Upload file
    var_url = var_base_url
    var_files = {'file': open(var_path, 'rb')}  
    var_response = requests.post(var_url, files = var_files)
    #
    ##  Execute detection
    var_url = str(var_response.url).replace("origin", "detect")
    var_response = requests.get(var_url)
    #
    ## Get the detection result
    var_name = var_url.split("/")[-1]
    var_url = var_base_url + "cache/" + var_name + "OUT.mp4"
    var_response = requests.get(var_url)
    #
    ## Save the result
    var_save_path = os.path.join(os.path.dirname(__file__), var_name + "OUT.mp4")
    with open(var_save_path,'wb') as var_file:
        var_file.write(var_response.content)
#
#
#
if __name__ == "__main__":
    var_url =  "http://219.223.194.37:8080/"
    auto_request(os.path.join(os.path.dirname(__file__), "cache", "test.mp4"), var_url)