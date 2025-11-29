import sys

from app import App

if __name__ == "__main__":
    app = App(sys.argv)
    try:
        app.mainloop()
    except Exception as error:
        pass
