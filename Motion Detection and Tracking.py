import cv2
import numpy as np
import argparse

def initialize_video_source(source=0):
    """Initialize video capture source (webcam or video file)."""
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise ValueError(f"Unable to open video source {source}")
    return cap

def process_frame(frame, bg_subtractor, min_area=500):
    """
    Process a single frame for motion detection.
    
    Args:
    - frame (numpy.ndarray): The current video frame.
    - bg_subtractor (cv2.BackgroundSubtractor): Background subtractor instance.
    - min_area (int): Minimum contour area to consider for motion.
    
    Returns:
    - frame_with_contours (numpy.ndarray): Frame with drawn contours.
    - fgmask (numpy.ndarray): Foreground mask from background subtraction.
    """
    # Apply the background subtractor to get the foreground mask
    fgmask = bg_subtractor.apply(frame)
    
    # Remove shadows by thresholding the mask
    _, fgmask = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
    
    # Apply morphological operations to clean the mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
    
    # Find contours in the thresholded mask
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw bounding boxes around significant contours
    for contour in contours:
        if cv2.contourArea(contour) >= min_area:
            # Filter contours based on aspect ratio and extent
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h
            extent = cv2.contourArea(contour) / (w * h)
            
            if 0.2 < aspect_ratio < 4.0 and extent > 0.3:  # Adjust these thresholds as needed
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    return frame, fgmask

def main(video_source=0, min_area=500):
    """Main function to capture video, process frames, and display the results."""
    cap = initialize_video_source(video_source)
    bg_subtractor = cv2.createBackgroundSubtractorKNN(history=500, dist2Threshold=400.0, detectShadows=True)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (640, 480))
            frame, fgmask = process_frame(frame, bg_subtractor, min_area)

            cv2.imshow('Motion Detection', frame)
            cv2.imshow('Foreground Mask', fgmask)

            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced Motion Detection and Tracking")
    parser.add_argument("-s", "--source", type=str, default="0",
                        help="Video source (0 for webcam or path to video file)")
    parser.add_argument("-a", "--min-area", type=int, default=500,
                        help="Minimum area size for detected motion")
    
    args = parser.parse_args()

    video_source = int(args.source) if args.source.isdigit() else args.source
    main(video_source=video_source, min_area=args.min_area)