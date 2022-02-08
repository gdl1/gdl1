# import required libraries
import sys
sys.path.append("/home/gdl1/vidgear")
from vidgear.gears import VideoGear
import numpy as np
import cv2

# open any valid video stream with stabilization enabled(`stabilize = True`)
stream_stab = VideoGear(source="/home/gdl1/Downloads/test_55.h264", stabilize=True).start()

# open same stream without stabilization for comparison
stream_org = VideoGear(source="/home/gdl1/Downloads/test_55.h264").start()

a = 1
captured_num = 0

# loop over
while True:

    # read stabilized frames
    frame_stab = stream_stab.read()

    # check for stabilized frame if Nonetype
    if frame_stab is None:
        break

    # read un-stabilized frame
    frame_org = stream_org.read()

    # concatenate both frames
    output_frame = np.concatenate((frame_org, frame_stab), axis=1)

    # put text over concatenated frame
    cv2.putText(
        output_frame,
        "Before",
        (10, output_frame.shape[0] - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2,
    )
    if a == 1:
        captured_num = captured_num + 1
        cv2.imwrite('/home/gdl1/frame_bef/'+str(captured_num)+'.jpg', frame_org)
    cv2.putText(
        output_frame,
        "After",
        (output_frame.shape[1] // 2 + 10, output_frame.shape[0] - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2,
    )
    if a == 1:
        captured_num = captured_num + 1
        cv2.imwrite('/home/gdl1/frame_aft/'+str(captured_num)+'.jpg', frame_stab)

    # Show output window
    cv2.imshow("Stabilized Frame", output_frame)

    

    # check for 'q' key if pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# close output window
cv2.destroyAllWindows()

# safely close both video streams
stream_org.stop()
stream_stab.stop()