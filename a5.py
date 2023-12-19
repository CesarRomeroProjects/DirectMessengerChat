# NAME: Cesar Damian Romero Amador
# EMAIL: cesardr1@uci.edu
# STUDENT ID: 31358030
import a5_gui as gui

def main():
    main_frame = gui.tk.Tk()
    main_frame.title("ICS 32 Distributed Social Messenger")
    main_frame.geometry("720x480")
    main_frame.option_add('*tearOff', False)
    app = gui.MainApp(main_frame)
    main_frame.update()
    main_frame.minsize(main_frame.winfo_width(), main_frame.winfo_height())
    num_id = main_frame.after(2000, app.check_new)
    print(num_id)
    main_frame.mainloop()


if __name__ == "__main__":
    main()
