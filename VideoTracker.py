import cv2
from random import randint

import scan


class VideoTracker:
    """Video Tracker Class"""
    trackerTypes = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']

    def __init__(self, video_path, tracker_type="CSRT", auto_calibrate=False, output_path='./test_output/output.mp4',
                 show_frame=False):
        """
        init video tracker
        :param video_path: Path of input video
        :param tracker_type: type of OpenCV tracker to use, CSRT seems to work the best so far and is default
        :param auto_calibrate: If True, will use pre-defined bounding boxes instead of manual
        :param output_path: Path of output video, will create if does not exist
        :param show_frame: If true, tracker displays the frame at each iteration
        """
        # Create a video capture object to read videos
        self.cap = cv2.VideoCapture(video_path)

        # video info
        self.vid_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.vid_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.n_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Output info
        self.output_path = output_path

        # Calibration of boxes
        if auto_calibrate:
            # use predefined bounding boxes
            bboxes, frame, colors = self.automatic_calibration()
        else:
            # manually draw bounding boxes
            bboxes, frame, colors = self.manual_calibration()

        # initialize multitracker object based on bounding boxes and selected tracker type
        multi_tracker = self.init_multitracker(bboxes, tracker_type, frame)

        # video saving format
        output_format = cv2.VideoWriter_fourcc(*'mp4v')

        # open and set properties
        video_out = cv2.VideoWriter()
        video_out.open(self.output_path, output_format, self.fps, (self.vid_width, self.vid_height), True)

        self.transformation_metadata = scan.get_transform_video(video_path, (11.5, 11.0))

        # run tracker and save video
        print(self.process_tracker(self.cap, multi_tracker, colors, video_out, show_frame))

    def init_multitracker(self, bboxes, tracker_type, frame):
        """
        Init an Opencv tracker instance, given a set of bounding boxes (e.g. one for each finger), and type
        :param bboxes: Bounding boxes
        :param tracker_type: E.g. CSRT
        :param frame: First frame, used for init
        :return: multitracker instance
        """
        # Create MultiTracker object
        multi_tracker = cv2.MultiTracker_create()

        # Initialize MultiTracker
        for bbox in bboxes:
            multi_tracker.add(self.create_tracker_by_name(tracker_type), frame, bbox)
        return multi_tracker

    def create_tracker_by_name(self, tracker_type):
        """
        Given input string, init the correct tracker
        :param tracker_type: e.g. 'CSRT'
        :return:
        """
        # Create a tracker based on tracker name
        if tracker_type == self.trackerTypes[0]:
            tracker = cv2.TrackerBoosting_create()
        elif tracker_type == self.trackerTypes[1]:
            tracker = cv2.TrackerMIL_create()
        elif tracker_type == self.trackerTypes[2]:
            tracker = cv2.TrackerKCF_create()
        elif tracker_type == self.trackerTypes[3]:
            tracker = cv2.TrackerTLD_create()
        elif tracker_type == self.trackerTypes[4]:
            tracker = cv2.TrackerMedianFlow_create()
        elif tracker_type == self.trackerTypes[5]:
            tracker = cv2.TrackerGOTURN_create()
        elif tracker_type == self.trackerTypes[6]:
            tracker = cv2.TrackerMOSSE_create()
        elif tracker_type == self.trackerTypes[7]:
            tracker = cv2.TrackerCSRT_create()
        else:
            tracker = None
            print('Incorrect tracker name')
            print('Available trackers are:')
            for t in self.trackerTypes:
                print(t)

        return tracker

    def read_first_frame(self):
        """
        Reads first frame for purposes of calibration & tracker init
        :return:
        """
        # Read first frame
        success, frame = self.cap.read()
        frame = cv2.resize(frame, (1920, 1080))
        self.vid_width = 1920
        self.vid_height = 1080

        # quit if unable to read the video file
        if not success:
            print('Failed to read video')
            raise Exception("Failed to read video")

        return frame

    def manual_calibration(self):
        """
        Manually draw bounding boxes
        :return: bounding boxes, first frame, color of each box
        """
        frame = self.read_first_frame()

        # Select boxes
        bboxes = []
        colors = []

        # OpenCV's selectROI function doesn't work for selecting multiple objects in Python
        # So we will call this function in a loop till we are done selecting all objects
        while True:
            # draw bounding boxes over objects
            # selectROI's default behaviour is to draw box starting from the center
            # when fromCenter is set to false, you can draw box starting from top left corner
            cv2.namedWindow('MultiTracker', 2)
            #cv2.setWindowProperty("MultiTracker",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

            bbox = cv2.selectROI('MultiTracker', frame)
            bboxes.append(bbox)
            colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
            print("Press q to quit selecting boxes and start tracking")
            print("Press any other key to select next object")
            k = cv2.waitKey(0) & 0xFF
            if k == 113:  # q is pressed
                break

        print('Selected bounding boxes {}'.format(bboxes))
        return bboxes, frame, colors

    def automatic_calibration(self):
        """
        Draw bounding boxes from predefined coordinates
        :return: bounding boxes, first frame, color of each box
        """
        defined_calibration_pts = [(371, 887, 77, 68),
                                   (571, 999, 99, 46),
                                   (692, 991, 111, 56),
                                   (801, 983, 95, 64),
                                   (998, 991, 93, 56),
                                   (1100, 981, 98, 66),
                                   (1248, 983, 101, 63),
                                   (1359, 881, 94, 60)]
        frame = self.read_first_frame()

        # Select boxes
        bboxes = []
        colors = []

        for this_box in defined_calibration_pts:
            bboxes.append(this_box)
            this_color = randint(0, 255), randint(0, 255), randint(0, 255)
            colors.append(this_color)

        return bboxes, frame, colors

    def generate_output_file(self, x_centers, y_centers):
        """
        Generates tab delimited output file
        :param x_centers: center of each box, x coord
        :param y_centers: center of each box, y coord
        :return:
        """
        with open('BrailleOutput.txt', 'w+') as outfile:
            outfile.write('Frame\tX Coordinate 1'
                          '\tY Coordinate 1'
                          '\tX Coordinate 2'
                          '\tY Coordinate 2'
                          '\tX Coordinate 3'
                          '\tY Coordinate 3'
                          '\tX Coordinate 4'
                          '\tY Coordinate 4'
                          '\tX Coordinate 5'
                          '\tY Coordinate 5'
                          '\tX Coordinate 6'
                          '\tY Coordinate 6'
                          '\tX Coordinate 7'
                          '\tY Coordinate 7'
                          '\tX Coordinate 8'
                          '\tY Coordinate 8\n')

            for i in range(len(x_centers)):
                row_data = str(i) + '\t'
                for box in range(8):
                    if box != 7:
                        row_data += str(x_centers[i][box]) + '\t' + str(y_centers[i][box]) + '\t'
                    else:
                        row_data += str(x_centers[8][box]) + '\t' + str(y_centers[8][box])
                    outfile.write(row_data + '\n')
        return x_centers, y_centers

    def process_tracker(self, cap, multi_tracker, colors, video_out, show_frame=False):
        """
        Given captured video & tracker object, track objects and output video + coordinates
        :param cap: OpenCV Cap object representing video stream
        :param multi_tracker: OpenCV tracker object
        :param colors: Colors of each bounding box
        :param video_out: Output video path
        :param show_frame: If True, program updates the frame during processing
        :return:
        """
        # Initialize Coordinate List
        x_centers = []
        y_centers = []
        frame_num = 0

        # Process video and track objects
        while cap.isOpened():
            x_centers_per_frame = [[]] * 8
            y_centers_per_frame = [[]] * 8

            success, frame = cap.read()
            try:
                if not success:
                    break
                frame = cv2.resize(frame, (1920, 1080))
            except Exception("Frame read failure"):
                break

            # get updated location of objects in subsequent frames
            success, boxes = multi_tracker.update(frame)

            # draw tracked objects
            for i, newbox in enumerate(boxes):
                p1 = (int(newbox[0]), int(newbox[1]))
                p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
                cv2.rectangle(frame, p1, p2, colors[i], 2, 1)

                x_center_pixel = boxes[i][0] + boxes[i][2] / 2
                y_center_pixel = boxes[i][1] + boxes[i][3] / 2

                x_centers_per_frame[i], y_centers_per_frame[i] = scan.transform_point((x_center_pixel, y_center_pixel), self.transformation_metadata)
                #x_centers_per_frame[i] = x_center_pixel
                #y_centers_per_frame[i] = y_center_pixel

            # add coordinates from this frame to overall coordinate list
            x_centers.append(x_centers_per_frame)
            y_centers.append(y_centers_per_frame)
            frame_num += 1

            # show frame
            if show_frame:
                cv2.imshow('MultiTracker', frame)
            video_out.write(frame)

            # quit on ESC button
            if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
                break

        x_centers, y_centers = self.generate_output_file(x_centers, y_centers)
        return x_centers, y_centers


if __name__ == '__main__':
    tracker = VideoTracker("./test_images/full_page2.MOV", auto_calibrate=False, show_frame=False)
