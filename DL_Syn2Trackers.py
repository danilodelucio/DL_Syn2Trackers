##### NUKE #####
import threading
import time

try:
    n = nuke.selectedNode()
    txtPath = n.knob("txt_path").getValue()
    print(txtPath)
    print()

    t_knob = int(n["T"].getValue())
    r_knob = int(n["R"].getValue())
    s_knob = int(n["S"].getValue())

    timeOffset = int(n.knob("TimeOffset").getValue())

    # Transform Settings (Initial Setup) // [Getting values]
    transform_get = int(n["transform"].getValue())
    reference_frame_get = n["reference_frame"].getValue()
    motionblur_get = n["motionblur"].getValue()
    shutter_get = n["shutter"].getValue()
    shutter_offset_get = int(n["shutteroffset"].getValue())

    if ".txt" in txtPath:
        # Manipulating the content of ".txt" file
        tracker_dict = {}
        with open(txtPath, "r") as txtFile:
            tracker_index = ""
            tracker_list = []
            for line in txtFile:
                tracker_data = line.strip().split(' ')
                if (len(tracker_data) == 1):
                    if (len(tracker_list) > 0):
                        tracker_dict[tracker_index] = tracker_list[:]
                        del tracker_list[:]
                    tracker_index = tracker_data[0]
                    continue
                else:
                    tracker_list.append(tracker_data)

        if (len(tracker_list) > 0):
            tracker_dict[tracker_index] = tracker_list[:]
            del tracker_list
            del tracker_index

        tracker_dict = sorted(tracker_dict.items())

        # Printing all Keys and Values separately from Dictionary
        count = 0
        for key in tracker_dict:
            print(key)
            count += 1
            print()

        # Creating a Tracker node, selecting him, and accessing the "tracks" knob
        dl_tracker = nuke.createNode("Tracker4")
        dl_tracker.knob("selected").setValue("True")
        n = nuke.selectedNode()

        # Transform Settings (Initial Setup) // [Setting values]
        transform_set = n["transform"].setValue(transform_get)
        reference_frame_set = n["reference_frame"].setValue(reference_frame_get)
        motionblur_set = n["motionblur"].setValue(motionblur_get)
        shutter_set = n["shutter"].setValue(shutter_get)
        shutter_offset_set = n["shutteroffset"].setValue(shutter_offset_get)

        tracks = n["tracks"]
        columns = 31

        tracker_id = -1
        for key, value in tracker_dict:

            # Starting Progress Bar
            task = nuke.ProgressTask("DL_Syn2Trackers")
            task.setMessage("Creating Trackers")
            time.sleep(0.5)
            if task.isCancelled():
                break
            task.setProgress(20)

            n['add_track'].execute()
            tracker_id += 1
            print("Tracker ID: " + str(tracker_id))
            print(key)
            print()

            for sublist in value:

                task.setProgress(40)

                frame_number = int(sublist[0]) + timeOffset
                print("Frame number: " + str(frame_number))
                tracker_x_value = float(sublist[1])
                print("X value: " + str(tracker_x_value))
                tracker_y_value = float(sublist[2])
                print("Y value: " + str(tracker_y_value))
                print()

                # Getting the "track_x" and "track_y" values from Tracker
                track_x_knob = tracker_id * columns + 2
                track_y_knob = tracker_id * columns + 3

                # Getting the "Translate/Rotate/Scale" columns from Tracker
                t_option = tracker_id * columns + 6
                r_option = tracker_id * columns + 7
                s_option = tracker_id * columns + 8

                # Setting a value on "track_x" / "track_y" [VALUE, FRAME, KNOB]
                tracks.setValueAt(tracker_x_value, frame_number, track_x_knob)
                tracks.setValueAt(tracker_y_value, frame_number, track_y_knob)

                # Setting the "T/R/S"
                if t_knob == 1:
                    tracks.setValue(1, t_option)
                else:
                    tracks.setValue(0, t_option)
                if r_knob == 1:
                    tracks.setValue(1, r_option)
                if s_knob == 1:
                    tracks.setValue(1, s_option)

                task.setProgress(70)

            task.setProgress(100)
            del task

    else:
        nuke.message('Invalid txt file! If you need help, please read the "How2Use" tab!')
except:
    nuke.message("Please keep the DL_Syn2Trackers node selected!")