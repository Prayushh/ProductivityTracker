import time
import threading
import sys

paused = False
main_clock_done = False

class DownClock:
    def __init__(self):
        self.start=input("Enter 'S' to start the timer: ")
    def display1(self, input_time):
        global main_clock_done
        secs = input_time * 60
        first_print = True
        if self.start.lower()=='s':
            while secs >= 0:
                mins, sec = divmod(secs, 60)
                timer = f"{mins:02d}:{sec:02d}"

                if not first_print:
                    sys.stdout.write('\033[2A')  # Move cursor up 2 lines
                else:
                    print("\n")  # Reserve 2 lines for consistent positioning
                    first_print = False

                sys.stdout.write(f"DownClock: {timer}      \n")
                sys.stdout.write("UpClock:   --:--      \n")
                sys.stdout.flush()

                secs -= 1
                time.sleep(1)
        else:
            print("Invalid character! ")

        main_clock_done = True
        print("\nTime's up !!!")


class UpClock:
    def display2(self, input_time):
        global main_clock_done, paused
        total_secs = input_time * 60
        secs = 0
        first_print = True

        while secs <= total_secs and not main_clock_done:
            if paused:
                time.sleep(0.1)
                continue

            mins, sec = divmod(secs, 60)
            timer = f"{mins:02d}:{sec:02d}"

            if not first_print:
                # Move cursor up 1 line to overwrite UpClock line only
                sys.stdout.write('\033[1A')
            else:
                first_print = False

            print(f"UpClock:   {timer}      ")  # spaces to clear leftover text

            secs += 1
            time.sleep(1)


input_time = int(input("Enter time you want to set for your work(in mins): "))

c1 = DownClock()
t1 = threading.Thread(target=c1.display1, daemon=True, args=(input_time,))
t1.start()

# Delay start of UpClock slightly so DownClock prints first
time.sleep(0.05)

c2 = UpClock()
t2 = threading.Thread(target=c2.display2,daemon=True, args=(input_time,))
t2.start()


def listen_for_pause():
    global main_clock_done, paused
    while not main_clock_done:
        cmd = input("Press 'P' to pause and 'R' to resume the timer: ")
        if cmd.lower() == 'p':
            paused = True
            print("Paused ⏸️")
        elif cmd.lower() == 'r':
            paused = False
            print("Resumed ▶️")
        else:
            print("Invalid choice! ")


try:
    listen_for_pause()
except KeyboardInterrupt:
    main_clock_done = True
    paused = True
    print("\nProgram interrupted by user. Exiting...")
    sys.exit()

t1.join()
t2.join()



    

    





