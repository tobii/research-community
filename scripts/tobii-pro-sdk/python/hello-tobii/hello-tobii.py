import time
import tobii_research as tr


def gaze_data_callback(gaze_data):
    left = gaze_data["left_gaze_point_on_display_area"]
    right = gaze_data["right_gaze_point_on_display_area"]
    print("Left eye: ({:.3f}, {:.3f}) \t Right eye: ({:.3f}, {:.3f})".format(
        left[0], left[1], right[0], right[1]))

def print_eyetrackers(eyetrackers):
    print("Eyetrackers found:")
    for eyetracker in eyetrackers:
        print(f"Index: {eyetrackers.index(eyetracker)}")
        print(f"\tAddress: {eyetracker.address}")
        print(f"\tModel: {eyetracker.model}")
        print(f"\tSerial number: {eyetracker.serial_number}\n")
        
def select_eyetracker(eyetrackers):
    while True:
        try:
            index = int(input("Select an eye tracker by index: "))
            if 0 <= index < len(eyetrackers):
                return eyetrackers[index]
            else:
                print("Invalid index. Please try again.")
        except ValueError:
            print("Please enter a valid integer index.")
              
def main():
    print("Looking for eye trackers...")
    found_eyetrackers = tr.find_all_eyetrackers()

    if not found_eyetrackers:
        print("No eye trackers found.")
        return

    print_eyetrackers(found_eyetrackers)
    eyetracker = select_eyetracker(found_eyetrackers)
    
    print(f"Using: {eyetracker.model} ({eyetracker.serial_number})")
    print(f"Address: {eyetracker.address}")
    print("Subscribing to gaze data. Press Ctrl+C to stop.\n")

    eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
        print("\nUnsubscribed. Done.")


if __name__ == "__main__":
    main()
