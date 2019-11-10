import cv2
from random import randint


class VideoTracker:
    """Video Tracker Class"""
    trackerTypes = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']

    def __init__(self, video_path, tracker_type="CSRT", auto_calibrate=False, output_path='./test_output/output.mp4'):
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
            bboxes, frame, colors = self.automatic_calibration()
        else:
            bboxes, frame, colors = self.manual_calibration()

        # initialize multitracker object based on bounding boxes and selected tracker type
        multi_tracker = self.init_multitracker(bboxes, tracker_type, frame)

        # video saving format
        output_format = cv2.VideoWriter_fourcc(*'mp4v')

        # open and set properties
        video_out = cv2.VideoWriter()
        video_out.open(self.output_path, output_format, self.fps, (self.vid_width, self.vid_height), True)

        # run tracker and save video
        self.process_tracker(self.cap, multi_tracker, colors, video_out)

    def init_multitracker(self, bboxes, tracker_type, frame):
        # Create MultiTracker object
        multi_tracker = cv2.MultiTracker_create()

        # Initialize MultiTracker
        for bbox in bboxes:
            multi_tracker.add(self.create_tracker_by_name(tracker_type), frame, bbox)
        return multi_tracker

    def create_tracker_by_name(self, tracker_type):
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

    def manual_calibration(self):
        # Read first frame
        success, frame = self.cap.read()
        frame = cv2.resize(frame, (1920, 1080))
        self.vid_width = 1920
        self.vid_height = 1080

        # quit if unable to read the video file
        if not success:
            print('Failed to read video')
            raise Exception("Failed to read video")

        # Select boxes
        bboxes = []
        colors = []

        # OpenCV's selectROI function doesn't work for selecting multiple objects in Python
        # So we will call this function in a loop till we are done selecting all objects
        while True:
            # draw bounding boxes over objects
            # selectROI's default behaviour is to draw box starting from the center
            # when fromCenter is set to false, you can draw box starting from top left corner
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
        pass
        return None, None, None

    def process_tracker(self, cap, multi_tracker, colors, video_out):
        # Process video and track objects
        while cap.isOpened():
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

            # show frame
            cv2.imshow('MultiTracker', frame)
            video_out.write(frame)

            # quit on ESC button
            if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
                break
        return True


if __name__ == '__main__':
    tracker = VideoTracker("./test_images/IMG_1285.MOV")




