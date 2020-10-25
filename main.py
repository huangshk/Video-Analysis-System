#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author       : Shuokang Huang
# @Organization : Peking University
# @Time         : 2020/10/25 23:00
#
#
#
import os, sys
import moviepy.editor as moviepy
from random import randint
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, make_response
from imageai.Detection import VideoObjectDetection
#
#
#
## Function to execute the object detection.
## Parameters:
## <var_in_path>    the path of video to perform object detection
## <var_out_path>   the path of output video
## <var_model_path> the path of detection model
def detect(var_name, var_model_path):
    #
    ##
    var_in_path = os.path.join(os.getcwd(), "cache", var_name + "IN.mp4")
    var_temp_path = os.path.join(os.getcwd(), "cache", var_name + "TEMP")
    # var_out_path = os.path.join(os.getcwd(), "cache", var_name + "OUT.mp4")
    #
    ##  Initiate the detector.
    var_detector = VideoObjectDetection()
    var_detector.setModelTypeAsRetinaNet()
    var_detector.setModelPath(var_model_path)
    var_detector.loadModel(detection_speed="fast")
    #
    ##  Perform the object detection.
    var_detector.detectObjectsFromVideo(input_file_path = var_in_path, 
                                        output_file_path = var_temp_path, 
                                        frames_per_second = 30, 
                                        log_progress = True, 
                                        frame_detection_interval = 1, 
                                        minimum_percentage_probability = 15)
    #
    ##  Convert the format of output video to MP4.
    var_clip = moviepy.VideoFileClip("cache/" + var_name + "TEMP.avi")
    var_clip.write_videofile("cache/" + var_name + "OUT.mp4")
    os.remove(var_temp_path + ".avi")
    return "Detect Finish!"
#
#
#
## Instantiate the system.
app = Flask(__name__, static_folder='', static_url_path='')
os.environ['CUDA_VISIBLE_DEVICES']= '0, 1, 2, 3'
#
#
#
## Function to render the index page.
@app.route('/', methods=['POST', 'GET'])
def app_index():
    #
    ## Initiate.
    print("app_index")
    if request.method == 'POST':
        var_name = str(randint(100000, 999999))
        var_file = request.files['file']
        var_path = os.path.join(os.path.dirname(__file__), "cache/" + var_name + "IN.mp4")
        var_file.save(var_path)
        return redirect(url_for('app_origin', var_name = var_name))

    return render_template("index.html")
#
#
#
## Function to present the original video.
@app.route('/origin/<var_name>')
def app_origin(var_name):
    #
    ## Initiate.
    print("app_origin")
    var_path = "/cache/" + var_name + "IN.mp4"
    print(var_path)
    return render_template("origin.html", var_name = var_name, var_path = var_path)
#
#
#
## Function to run the object detection.
@app.route("/detect/<var_name>")
def app_detect(var_name):
    #
    ## Initiate.
    print("app_detect")
    var_model_path = os.path.join(os.getcwd(), "models", "resnet50_coco_best_v2.0.1.h5")
    var_in_path = os.path.join(os.getcwd(), "cache", var_name + "IN.mp4")
    var_out_path = os.path.join(os.getcwd(), "cache", var_name + "OUT.mp4")
    var_render_path = "/cache/" + var_name + "OUT.mp4"
    #
    ##
    if(not os.path.exists(var_in_path)):
        return redirect(url_for('app_index'))
    else:
        #
        ## Perform the detection if the video has not been execute detection.
        if(not os.path.exists(var_out_path)):
            detect(var_name, var_model_path)
        #
        ## Render the result.
        return render_template("detect.html", var_name = var_name, var_render_path = var_render_path)
#
#
#
## Function to run the object detection.
@app.route("/extract/<var_name>")
def app_extract(var_name):
    #
    ## Initiate.
    print("app_extract")
    var_in_path = os.path.join(os.getcwd(), "cache", var_name + "IN.mp4")
    #
    ## Redirect to the index page if no video has been uploaded.
    if(not os.path.exists(var_in_path)):
        return redirect(url_for('app_index'))
    else:
        #
        ## Extract the audio from the video and download it.
        var_clip = moviepy.VideoFileClip("cache/" + var_name + "IN.mp4")
        var_audio = var_clip.audio
        var_audio.write_audiofile("cache/" + var_name + "OUT.mp3")
        var_filename = var_name + "OUT.mp3"
        var_path = os.path.join(os.getcwd(), "cache")
        var_response = make_response(send_from_directory(var_path, var_filename, as_attachment=True))
        var_response.headers["Content-Disposition"]="attachment; filename={}".format(var_filename.encode().decode('latin-1'))
        os.remove(os.path.join(os.getcwd(), "cache", var_name + "OUT.mp3"))
        return var_response
#
#
#
## Function to restart.
@app.route('/restart/<var_name>')
def app_restart(var_name):
    #
    ##
    print("app_restart")
    #
    ##
    var_in_path = os.path.join(os.getcwd(), "cache", var_name + "IN.mp4")
    var_out_path = os.path.join(os.getcwd(), "cache", var_name + "OUT.mp4")
    #
    ##
    if(os.path.exists(var_in_path)):
        os.remove(var_in_path)
    if(os.path.exists(var_out_path)):    
        os.remove(var_out_path)
    #
    ##
    return redirect(url_for('app_index'))
#
#
#
## Main function to run the system
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)