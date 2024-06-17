# VERSION 0.3, 31/OCT/2023

# imported libraries
import csv

import graphics as gr
import properties as prop
from tkinter import StringVar, BooleanVar, filedialog
import cv2
from datetime import datetime
import cameras

# Variables and Booleans
file_loc = ""
file_selected = False
vehicle_selected = False
data_saved = False

# Variables and declerations for video recording
recording = False
video_writer = None
current_datetime = datetime.now()




# data saving dictionaries
dat_dict = {}
disp_dict = {}

recording = False
video_writer = None
resized_frame = None


def toggle_recording():
    global recording, video_writer, resized_frame

    if recording:
        # Stop recording
        if video_writer is not None:
            video_writer.release()
            video_writer = None
            print("Recording stopped.")
        recording = False
    else:
        # Start recording
        if resized_frame is None:
            print("Error: No frame to record.")
            return

        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")
        output_file = f"recordings/{formatted_datetime}.avi"

        fps = 30  # Change this to desired frames per second (FPS)
        codec = cv2.VideoWriter_fourcc(*'XVID')  # Codec for AVI file format
        video_writer = cv2.VideoWriter(output_file, codec, fps, (resized_frame.shape[1], resized_frame.shape[0]))
        recording = True
        print(f"Recording started. Saving to {output_file}")


# def toggle_recording():
#     formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")
#     output_file = f"recordings/{formatted_datetime}.avi"  # Change this to desired video output file path
#     global recording, video_writer, resized_frame
#
#     if recording:
#
#         # Stop recording
#         if video_writer is not None:
#             video_writer.release()
#             video_writer = None
#             print("Recording stopped.")
#         recording = False
#     else:
#         # Start recording
#         if resized_frame is None:
#             print("Error: No frame to record.")
#             return
#
#         fps = 30  # Change this to desired frames per second (FPS)
#         codec = cv2.VideoWriter_fourcc(*'XVID')  # Codec for AVI file format
#         video_writer = cv2.VideoWriter(output_file, codec, fps, (resized_frame.shape[1], resized_frame.shape[0]))
#         recording = True
#         print("Recording started.")




# function
def destroy_window():
    """Destroys the window, shows warning errors, and opens the POV Camera."""
    global file_selected, vehicle_selected, data_saved

    if file_selected and vehicle_selected and data_saved:
        res = message.confirm_message(text="Do you want to continue?")
        if res:
            win.win_destroy()
    elif not file_selected and vehicle_selected:
        message.error_message(text="Log File not selected!")
    elif not vehicle_selected and file_selected:
        message.error_message(text="Vehicle Type not selected!")
    elif not file_selected and not file_selected:
        message.error_message(text="Select Log File and Vehicle Type!")
    elif not data_saved:
        message.error_message(text="Data not saved!")


def open_file_dialog():
    """This function open the Windows file explorer."""
    global file_loc, file_selected
    file_p = filedialog.askopenfile(filetypes=[("CSV Files", "*.csv")])
    if file_p:
        entry_var.set(file_p.name)
        file_loc = file_p.name
        file_selected = True


def veh_disp(event):
    """Displays the selected vehicle on dummy screen"""
    global vehicle_selected
    dummy_can.del_text("veh")
    choice = vehicle_var.get()
    if choice == prop.VEHICLE_OPTIONS[0]:
        dummy_can.add_text(840 // 2, 60, text=choice, anc="n", font=(prop.FONT_STYLE, 10), tag="veh",
                           fill=prop.SCREEN_BG)
        vehicle_selected = True
    elif choice == prop.VEHICLE_OPTIONS[1]:
        dummy_can.add_text(840 // 2, 60, text=choice, anc="n", font=(prop.FONT_STYLE, 10), tag="veh",
                           fill=prop.SCREEN_BG)
        dummy_can.add_text(805 // 2, 85, text="   V\nm/sec", anc="nw", fill=prop.SCREEN_BG, tag="veh",
                           font=(prop.FONT_STYLE, 10))
        vehicle_selected = True
    elif choice == prop.VEHICLE_OPTIONS[2]:
        dummy_can.add_text(840 // 2, 60, text=choice, anc="n", font=(prop.FONT_STYLE, 10), tag="veh",
                           fill=prop.SCREEN_BG)
        dummy_can.add_text(805 // 2, 85, text="   V\nm/sec", anc="nw", fill=prop.SCREEN_BG, tag="veh",
                           font=(prop.FONT_STYLE, 10))
        vehicle_selected = True


def update_disp():
    """Updates the dummy screen, after selection on checkbox."""
    # 1. rate of climb
    if roc_s.get():
        dummy_can.add_text(x=348, y=85, text=" ROC\nm/sec", tag="roc", anc="nw", fill=prop.SCREEN_BG,
                           font=(prop.FONT_STYLE, 10))
    else:
        dummy_can.del_text("roc")
    # 2. flight time
    if temp_s.get():
        dummy_can.add_text(x=455, y=85, text=" T\n°C", tag="ft", anc="nw", fill=prop.SCREEN_BG,
                           font=(prop.FONT_STYLE, 10))
    else:
        dummy_can.del_text("ft")
    # 3. lat long
    if ll_s.get():
        dummy_can.add_text(x=780, y=440, text="_°N\n_°W", tag="ll", anc="nw", fill=prop.SCREEN_BG,
                           font=(prop.FONT_STYLE, 10))
    else:
        dummy_can.del_text("ll")
    # 4. pitch rate
    if pr_s.get():
        dummy_can.add_text(x=40, y=200, text="p.\n_°/sec", tag="pr", anc="nw", fill=prop.SCREEN_BG,
                           font=(prop.FONT_STYLE, 10))
    else:
        dummy_can.del_text("pr")
    # 5. roll rate
    if rr_s.get():
        dummy_can.add_text(x=40, y=240, text="r.\n_°/sec", tag="rr", anc="nw", fill=prop.SCREEN_BG,
                           font=(prop.FONT_STYLE, 10))
    else:
        dummy_can.del_text("rr")
    # 6. yaw rate
    if yr_s.get():
        dummy_can.add_text(x=40, y=280, text="y.\n_°/sec", tag="yr", anc="nw", fill=prop.SCREEN_BG,
                           font=(prop.FONT_STYLE, 10))
    else:
        dummy_can.del_text("yr")
    # 7. esc data
    if esc_s.get():
        dummy_can.add_text(x=40, y=340, text="ESC\nrpm|A|V", tag="esc", anc="nw", fill=prop.SCREEN_BG,
                           font=(prop.FONT_STYLE, 10))
    else:
        dummy_can.del_text("esc")


def save_settings():
    """Saves the changes made in settings tab."""
    global data_saved, dat_dict
    if vehicle_selected and file_selected:
        res = message.confirm_message(text="Save settings?")
        dat_dict = {"File location": file_loc, "vehicle type": vehicle_var.get(), "climbRate": roc_s.get(),
                    "temperature.temperature1": temp_s.get(),
                    "gps.lat_lon": ll_s.get(), "rollRate": rr_s.get(), "pitchRate": pr_s.get(), "yawRate": yr_s.get(),
                    "escStatus.": esc_s.get()}
        if res:
            data_saved = True
    elif not vehicle_selected and file_selected:
        message.warn_message(text="Vehicle type not selected!")
    elif not file_selected and vehicle_selected:
        message.warn_message(text="Log file not selected!")
    elif not file_selected and not vehicle_selected:
        message.warn_message(text="Vehicle type and Log file not selected!")


# messages method
message = gr.Message()

# setting main window
win = gr.GWindow()
win.start_window()

# placing logo on top left
logo_can = gr.GCanvas(win, width=126, height=50, bg=prop.SCREEN_BG)
logo_can.add_image("images/amrita.png", x=0, y=0, scale=4)
logo_can.place_canvas(place_y=0, place_x=0)

# seperator line
gr.seperator(0, 50, ref="raised")
gr.seperator(0, 600, ref="raised")
gr.seperator(880, 55, width=2, height=542, ref="raised")

# canvas for dummy screen
dummy_can = gr.GCanvas(win, width=835, height=505, ref="sunken")
dummy_can.place_canvas(place_x=15, place_y=70)
# rectangle to place label
head_rect = dummy_can.add_rect(x0=1, y0=1, x1=838, y1=30)
head_label = dummy_can.add_text(x=838 / 2, y=8, text="Sample screen", anc="n")

# dummy screen
dummy_screen = dummy_can.add_rect(x0=20, y0=40, x1=825, y1=497, fill="black")

# canvas for file selector
file_can = gr.GCanvas(win, width=250, height=100, ref="sunken")
file_can.place_canvas(place_x=910, place_y=70)
# rectangle to place label
fs_rect = file_can.add_rect(x0=1, y0=1, x1=252, y1=30)
fs_label = file_can.add_text(x=250 / 2, y=8, text="File Selector", anc="n")
# button to select file
fs_button = file_can.add_button(text="Select file", comm=open_file_dialog, place_x=10, place_y=55, anc="w")
# entry box to display selected file address
entry_var = StringVar()
fs_entry = file_can.add_entry(text_var=entry_var, width=40, place_x=130, place_y=85, anc="center")

# canvas for settings
sett_can = gr.GCanvas(win, width=250, height=375, ref="sunken")
sett_can.place_canvas(place_x=910, place_y=200)
# rectangle to place label
sett_can.add_rect(x0=1, y0=1, x1=253, y1=30)
sett_can.add_text(x=250 / 2, y=8, text="Settings", anc="n")

# options in settings
# 1 vehicle selection
sett_can.add_text(x=30, y=55, text="Vehicle type: ", anc="nw", font=(prop.FONT_STYLE, 10))
dummy_can.add_text(x=840 // 2, y=60, text="- - - - - -", anc="n", font=(prop.FONT_STYLE, 10), fill=prop.SCREEN_BG,
                   tag="veh")
vehicle_var = StringVar()
vehicle_list = prop.VEHICLE_OPTIONS
vehicle_var.set(vehicle_list[0])
sett_can.add_combo(var=[vehicle_var], opts=vehicle_list, place_x=115, place_y=55, anc="nw", width=15, comm=veh_disp)

# 2 rate of climb
sett_can.add_text(x=30, y=95, text="RoC: ", anc="nw", font=(prop.FONT_STYLE, 10))
roc_s = BooleanVar()
sett_can.add_checkbox(var=roc_s, comm=update_disp, place_x=110, place_y=90)

# 3 temperature
sett_can.add_text(x=30, y=130, text="Temperature: ", anc="nw", font=(prop.FONT_STYLE, 10))
temp_s = BooleanVar()
sett_can.add_checkbox(var=temp_s, comm=update_disp, place_x=110, place_y=125)

# 4 latitude and longitude
sett_can.add_text(x=30, y=165, text="Lat.-Long.: ", anc="nw", font=(prop.FONT_STYLE, 10))
ll_s = BooleanVar()
sett_can.add_checkbox(var=ll_s, comm=update_disp, place_x=110, place_y=160)

# 5 pitch rate
sett_can.add_text(x=30, y=200, text="Pitch rate: ", anc="nw", font=(prop.FONT_STYLE, 10))
pr_s = BooleanVar()
sett_can.add_checkbox(var=pr_s, comm=update_disp, place_x=110, place_y=195)

# 6 roll rate
sett_can.add_text(x=30, y=235, text="Roll rate: ", anc="nw", font=(prop.FONT_STYLE, 10))
rr_s = BooleanVar()
sett_can.add_checkbox(var=rr_s, comm=update_disp, place_x=110, place_y=230)

# 7 Yaw rate
sett_can.add_text(x=30, y=270, text="Yaw rate: ", anc="nw", font=(prop.FONT_STYLE, 10))
yr_s = BooleanVar()
sett_can.add_checkbox(var=yr_s, comm=update_disp, place_x=110, place_y=265)

# 8 esc
sett_can.add_text(x=30, y=305, text="ESC: ", anc="nw", font=(prop.FONT_STYLE, 10))
esc_s = BooleanVar()
sett_can.add_checkbox(var=esc_s, comm=update_disp, place_x=110, place_y=300)

# 9 save button
sett_can.add_button(place_x=30, place_y=340, text="Save", anc="nw", comm=save_settings)

# 10 exit
sett_can.add_button(text="Start", place_x=190, place_y=340, anc="nw", comm=destroy_window)

# mandatory parameters on screen
# 1. real time and date
dummy_can.add_text(40, 60, text="HH:MM:SS\n dd/mm/yy", fill=prop.SCREEN_BG, font=(prop.FONT_STYLE, 10), anc="nw")

# 2. vehicle fly time
dummy_can.add_text(730, 60, text="FLIGHT TIME\n    00:00:00", font=(prop.FONT_STYLE, 10), fill=prop.SCREEN_BG, anc="nw")

# 3. battery
dummy_can.add_text(750, 120, text="  BATT\n_ _._V\n_ _._mAh", anc="nw", fill=prop.SCREEN_BG, font=(prop.FONT_STYLE, 10))

# 4. reference line
gr.seperator(place_x=285, place_y=340, width=300, height=2, bg=prop.SCREEN_BG)

# 5. roll line
roll = gr.GCanvas(win, width=250, height=65, bg="black", hb="black")
roll.add_image(file_path="images/roll_val.png", x=0, y=0, scale=3)
roll.place_canvas(place_x=350, place_y=220)
dummy_can.add_text(410, 135, text="roll", anc="nw", font=(prop.FONT_STYLE, 10), fill=prop.SCREEN_BG)

# 6. pitch line
pitch = gr.GCanvas(win, width=60, height=250, bg="black", hb="black")
pitch.add_image(file_path="images/pitch_val.png", x=0, y=20, scale=3)
pitch.place_canvas(place_x=625, place_y=215)
dummy_can.add_text(630, 130, text="pitch", anc="nw", font=(prop.FONT_STYLE, 10), fill=prop.SCREEN_BG)

# 7. alt line
alt = gr.GCanvas(win, width=60, height=250, bg="black", hb="black")
alt.add_image(file_path="images/alt_val.png", x=10, y=20, scale=3)
alt.place_canvas(place_x=180, place_y=215)
dummy_can.add_text(185, 130, text="alt", anc="nw", font=(prop.FONT_STYLE, 10), fill=prop.SCREEN_BG)

# 8. heading
head = gr.GCanvas(win, width=250, height=65, bg="black", hb="black")
head.add_image(file_path="images/dir_val.png", x=10, y=10, scale=3)
head.place_canvas(place_x=320, place_y=455)
dummy_can.add_text(410, 365, text="heading", anc="nw", font=(prop.FONT_STYLE, 10), fill=prop.SCREEN_BG)

# loop to run window
win.loop()

"""Open the pov camera and reading data from the selected file."""
# creating a new dictionary only for selected items
for key, value in dat_dict.items():
    if value:
        disp_dict[key] = value


def load_csv_data(head_list):
    """Loads the data from csv to list."""
    packed_dict = {}
    try:
        with open(file_loc, 'r') as csvfile:
            # read csv file
            csvfile.seek(0, 2)
            end_pos = csvfile.tell()

            # setting position and reading from end of file
            pos = end_pos - 2
            while pos > 0 and csvfile.read(1) != '\n':
                pos -= 1
                csvfile.seek(pos)

            # read and split last line
            last_line = csvfile.readline()
            last_row_values = last_line.strip().split(',')

            # column name from required list
            csvfile.seek(0)
            top = next(csv.reader(csvfile, delimiter=',', quotechar='"'))

            # packing the values found in the csv file
            found_data = [last_row_values[top.index(c)] if top and c in top else None for c in head_list]
            for k, v in zip(head_list, found_data):
                packed_dict[k] = v

            return packed_dict
    except FileNotFoundError:
        return {"error": f"The file {file_loc} does not exist."}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}


def info_disp(fr, text, x, y, size=0.75):
    """Displays text on frame."""
    cv2.putText(fr, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, size, (255, 255, 255), 2)


def place_image(fr, image, position, size):
    """Places the image on frame."""
    image_resized = cv2.resize(image, size)

    # Get the dimensions of the image
    height, width, _ = image_resized.shape

    # Ensure the position fits within the frame boundaries
    if position[0] + height > fr.shape[0] or position[1] + width > fr.shape[1]:
        print(f"Image exceeds frame boundaries at position {position} with size {size}")
        return

    # Get the region of interest (ROI) on the frame to place the image
    roi = fr[position[0]:position[0] + height, position[1]:position[1] + width]

    # Create a mask for the image
    image_gray = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(image_gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    # Place the image on the frame
    img_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    img_fg = cv2.bitwise_and(image_resized, image_resized, mask=mask)
    dst = cv2.add(img_bg, img_fg)

    # Update the frame with the placed image
    fr[position[0]:position[0] + height, position[1]:position[1] + width] = dst


def place_info():
    """Places the relevant info on screen."""
    rec_dict = load_csv_data(sel_col)

    if "error" in rec_dict:
        info_disp(resized_frame, f"{rec_dict['error']}", 1200 // 2, 675 // 2)
        return resized_frame
    else:
        # time and date
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%d/%m/%y")
        info_disp(resized_frame, f" {current_time}", 20, 30)
        info_disp(resized_frame, f"{current_date}", 20, 60)

        # flight time
        info_disp(resized_frame, "Flight Time", 1070, 30)
        info_disp(resized_frame, rec_dict["flightTime"], 1090, 60)

        # battery status
        info_disp(resized_frame, "BATT", 1110, 130)
        info_disp(resized_frame, "__._V", 1110, 160)
        info_disp(resized_frame, "__._mAh", 1090, 190)

        # roll values
        info_disp(resized_frame, rec_dict["roll"], 640, 150, size=0.5)
        # altitude values
        info_disp(resized_frame, f"{rec_dict['altitudeAMSL']}m", 345, 400, size=0.4)
        # pitch values
        info_disp(resized_frame, f"{rec_dict['pitch']}", 935, 400, size=0.5)
        # dir values
        info_disp(resized_frame, f"{rec_dict['heading']}", 655, 650, size=0.5)

        if recording:
            cv2.circle(resized_frame, (20, 20), 10, (0, 0, 255), -1)  # Draw red circle for recording indicator

        # processing saved data
        for keys, vals in disp_dict.items():
            # condition to display vehicle type
            if keys == "vehicle type":
                info_disp(resized_frame, vals, 615, 30)
                # vehicle speed from csv file
                if vals != prop.VEHICLE_OPTIONS[0]:
                    info_disp(resized_frame, " V", 615, 60)
                    info_disp(resized_frame, f"{rec_dict['airSpeed']} m/sec", 610, 80)
            # condition to display rate of climb
            if keys == prop.PARAM_LIST[6]:
                info_disp(resized_frame, " ROC", 500, 60)
                info_disp(resized_frame, f"{rec_dict['climbRate']} m/sec", 440, 80)
            # condition to display temperature
            if keys == prop.PARAM_LIST[7]:
                info_disp(resized_frame, " T", 785, 60)
                info_disp(resized_frame, f"{round(float(rec_dict['temperature.temperature1']), 2)} C", 785, 80)
            # condition to display lat lon
            if keys == prop.PARAM_LIST[8]:
                info_disp(resized_frame, f"{round(float(rec_dict['gps.lat']), 2)}N", 1100, 640)
                info_disp(resized_frame, f"{round(float(rec_dict['gps.lon']), 2)}W", 1100, 670)
            # condition to display roll rate
            if keys == prop.PARAM_LIST[9]:
                info_disp(resized_frame, "r.", 20, 330)
                info_disp(resized_frame, f"{rec_dict['rollRate']}/sec", 20, 360)
            # condition to display pitch rate
            if keys == prop.PARAM_LIST[10]:
                info_disp(resized_frame, "p.", 20, 270)
                info_disp(resized_frame, f"{rec_dict['pitchRate']}/sec", 20, 300)
            # condition to display yaw rate
            if keys == prop.PARAM_LIST[11]:
                info_disp(resized_frame, "y.", 20, 390)
                info_disp(resized_frame, f"{rec_dict['yawRate']}/sec", 20, 420)
            # condition to display esc status
            if keys == prop.PARAM_LIST[12]:
                info_disp(resized_frame, "ESC", 20, 470)
                info_disp(resized_frame, "| rpm | A | V |", 20, 500)
                p = 530
                for m in range(len(esc_avail) // 3):
                    rpm = round(float(rec_dict[f'escStatus.rpm{m + 1}']), 2)
                    amp = round(float(rec_dict[f'escStatus.current{m + 1}']), 2)
                    vol = round(float(rec_dict[f'escStatus.voltage{m + 1}']), 2)
                    info_disp(resized_frame, f"|{rpm}|{amp}|{vol}|", 20, p)
                    p += 30

    return resized_frame



# if data_saved:
# creating a list for selected params
sel_col = ['airSpeed', 'flightTime', 'roll', 'altitudeAMSL', 'pitch', 'heading']
esc = []
esc_avail = []

for key, val in disp_dict.items():
    if val is True:
        # setting gps headers
        if key == "gps.lat_lon":
            sel_col.extend(['gps.lat', 'gps.lon'])
        else:
            sel_col.append(key)
        # checking number of esc present in csv file.
        if key == 'escStatus.':
            sel_col.remove('escStatus.')
            # creating a esc list
            esc_rpm = ['escStatus.rpm' + str(val) for val in range(1, 9)]
            esc_amp = ['escStatus.current' + str(val) for val in range(1, 9)]
            esc_volt = ['escStatus.voltage' + str(val) for val in range(1, 9)]
            esc = esc_rpm + esc_amp + esc_volt
            with open(file_loc, 'r') as c_file:
                c_read = csv.reader(c_file)
                header = next(c_read, None)
                for i in range(len(esc)):
                    for col in header:
                        if esc[i] == col:
                            esc_avail.append(col)
# list for all headers
sel_col += esc_avail

# load images
roll_image = cv2.imread("images/roll_val.png")
alt_image = cv2.imread("images/alt_val.png")
pitch_image = cv2.imread("images/pitch_val.png")
dir_image = cv2.imread("images/dir_val.png")

# opens the pov camera after settings saved
cap = cv2.VideoCapture(cameras.main())

# loop to show cam frame
while True:
    # captures the camera to show as frame
    ret, frame = cap.read()

    resized_frame = cv2.resize(frame, None, fx=1.875, fy=1.40625)

    # Check if recording is active
    if recording:
        # Write the frame to the video file
        if video_writer is not None:
            video_writer.write(resized_frame)

    # displays the text and parameters on screen
    resized_frame = place_info()
    if recording:
        cv2.circle(resized_frame, (20, 20), 10, (0, 0, 255), -1)  # Draw red circle for recording indicator

    # images on frame
    place_image(resized_frame, roll_image, (120, 480), (357, 92))
    place_image(resized_frame, alt_image, (200, 330), (105, 408))
    place_image(resized_frame, pitch_image, (200, 880), (105, 408))
    place_image(resized_frame, dir_image, (610, 480), (363, 93))

    # displays the frame
    cv2.imshow('Camera Feed', resized_frame)


    # Check for events (key press or window closed)
    key = cv2.waitKey(1)

    # Check if a key is pressed or if the window is closed
    if key != -1:  # key pressed
        if key == ord('r'):  # Check if the key is 'r'
            toggle_recording()  # Start/stop recording without passing any arguments
        elif key == 27:  # Check if the key is ESC (ASCII value 27)
            break  # Exit loop if ESC is pressed
    else:  # No key pressed (key == -1)
        # Check if the window is closed by checking the window property
        if cv2.getWindowProperty('Camera Feed', cv2.WND_PROP_VISIBLE) < 1:
            break  # Exit loop if window is closed


# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
