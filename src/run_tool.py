import csv_handler
import cml_interface
import os


class color:
    """Defines different colors and text formatting settings to be used for CML output printing."""

    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def run_project():
    run_dec = input(
        color.BOLD
        + color.UNDERLINE
        + "{*} Enter C to run Command Line Interface or U to run the User Interface:"
        + color.END
        + color.END
        + "  "
    )

    if run_dec == "C":
        cml_interface.run_cml()
    elif run_dec == "U":
        print("If in DOCKER: http://localhost:8501")
        
        os.system("streamlit run web_app.py")
        print("Will run the UI to be implemented in the near future.")
    else:
        print(
            color.RED
            + color.BOLD
            + "{!!} Invalid option chosen! Running the CML..."
            + color.END
            + color.END
        )
        cml_interface.run_cml()


run_project()
